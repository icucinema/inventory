var app = angular.module('InventoryApp', [
	'ngRoute',
	'ngAnimate',
	'ngAnimate-animate.css',
	'restangular'
]);

app.constant('djurl', __djurls);

app.config(['djurl', '$routeProvider', '$httpProvider', 'RestangularProvider', function(djurl, $routeProvider, $httpProvider, RestangularProvider) {
	RestangularProvider.setResponseExtractor(function(response, operation, what, url) {
		if (operation === "getList") {
			// Use results as the return type, and save the result metadata
			// in _resultmeta
			if (!response.results) return response;
			var newResponse = response.results;
			newResponse._resultmeta = {
				"count": response.count,
				"next": response.next,
				"previous": response.previous,
			};
			return newResponse;
		}
		
		return response;
	});
	RestangularProvider.setBaseUrl(djurl.api_root);
	RestangularProvider.setRequestSuffix('/');
	RestangularProvider.setRestangularFields({
		selfLink: 'url'
	});
	$routeProvider.
		when('/', {
			templateUrl: djurl.partial_root + 'index.html',
			controller: 'IndexCtrl'
		}).
		when('/item', {
			templateUrl: djurl.partial_root + 'items.html',
			controller: 'ItemsCtrl'
		}).
    	when('/item/add', {
			templateUrl: djurl.partial_root + 'additem.html',
			controller: 'ItemAddCtrl'
		}).
		when('/item/:id', {
			templateUrl: djurl.partial_root + 'item.html',
			controller: 'ItemCtrl'
		}).
		otherwise({
			redirectTo: '/'
		});
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

app.directive('ngConfirmClick', [
  function(){
    return {
      priority: -1,
      restrict: 'A',
      link: function(scope, element, attrs){
        element.bind('click', function(e){
          var message = attrs.ngConfirmClick;
          if(message && !confirm(message)){
            e.stopImmediatePropagation();
            e.preventDefault();
          }
        });
      }
    }
  }
]);
app.directive('tabs', function() {
	return {
		restrict: 'E',
		scope: {},
		transclude: true,
		template: '<section class="tabs"><ul class="tab-nav"><li ng-repeat="pane in panes" ng-class="{active: pane.active}"><a href ng-click="select(pane)">{{ pane.tabTitle }}</a></li></ul><div ng-transclude></div></section>',
		controller: function($scope) {
			var panes = $scope.panes = [];
			$scope.select = function(pane) {
				angular.forEach(panes, function(pane) {
					pane.active = false;
				});
				pane.active = true;
			};
			this.addPane = function(pane) {
				if (panes.length == 0) {
					$scope.select(pane);
				}
				panes.push(pane);
			};
			$scope.$parent.panes = {
				panes: $scope.panes,
				select: $scope.select
			};
		}
	}
});
app.directive('tab', function() {
	return {
		restrict: 'E',
		scope: {
			tabTitle: '@'
		},
		transclude: true,
		template: '<div class="tab-content" ng-class="{active: active}" ng-transclude></div>',
		require: '^tabs',
		link: function(scope, element, attrs, tabsCtrl) {
			tabsCtrl.addPane(scope);
		}
	}
});

app.controller('AppCtrl', function($scope) {
	$scope.hBack = function() { 
		window.history.go(-1);
	};
});
app.controller('NavCtrl', function($scope) {
	$scope.navs = [
/*
		{
			'name': 'index',
			'url': '/',
			'text': 'Index'
		},
*/
		{
			'name': 'item',
			'url': '/item',
			'text': 'List Items'
		},
        {
            'name': 'additem',
            'url': '/item/add',
            'text': 'Add Item'
        },
	];

	$scope.navActive = function(navName) {
		if ($scope.navName == navName) return 'active';
		return '';
	}
});
app.controller('IndexCtrl', function($rootScope) {
	$rootScope.navName = 'index';
});
app.controller('ItemsCtrl', function($rootScope, $scope, $routeParams, $location, Restangular) {
	$rootScope.navName = 'item';

	var thisPage = parseInt($routeParams.page, 10);
	if (thisPage != $routeParams.page) {
		$location.search('page', 1);
		return;
	}

	var perPage = parseInt($routeParams.perPage, 10);
	if (isNaN(perPage) || perPage < 5) {
		perPage = 10;
	}
	var sobj = {
		page: thisPage,
		per_page: perPage
	};

	var items = Restangular.all('item');
	var updateItemData = function() {
        	items.getList(sobj).then(function(res) {
			var startRecord = ((thisPage-1) * perPage) + 1;
			var endRecord = (startRecord + res.length) - 1;
			$scope.data = {
				'startAt': startRecord,
				'endAt': endRecord,
				'results': res,
				'next': (res._resultmeta.next ? thisPage+1 : null),
				'previous': (res._resultmeta.previous ? thisPage-1 : null),
				'count': res._resultmeta.count
			}
		});
	};
	updateItemData();

	$scope.search = function(q) {
		sobj.search = q;
		updateItemData();
	};

	$scope.goTo = function(where) {
		if (!where) return;
		$location.search('page', where);
	};

	$scope.buttonClass = function(pageNum) {
		if (!pageNum) return 'default';
		return 'secondary';
	};

	$scope.itemUrl = function(item) {
		return '#/item/' + item.id;
	};
});
app.controller('ItemCtrl', function($rootScope, $scope, $filter, $routeParams, $location, Restangular, $timeout) {
	$rootScope.navName = 'item';

	$scope.loading = true;
    $scope.editing = false;

	var itemId = parseInt($routeParams.id, 10);

	var item = Restangular.one('item', itemId);
	item.get().then(function(res) {
		$scope.loading = false;
		$scope.data = res;
	});
    var updateNotesData = function() {
        item.getList('notes').then(function(res) {
            $scope.notes = res;
        });
    };
    updateNotesData();
    item.getList('pictures').then(function(res) {
		$scope.pictures = res;
	});
    item.getList('quotes').then(function(res) {
		$scope.quotes = res;
	});


    var suppliers = Restangular.all('supplier');
    suppliers.getList().then(function(res) {
        $scope.suppliers = res;
    });

    var itemCategories = Restangular.all('itemcategory');
    itemCategories.getList().then(function(res) {
        $scope.itemCategories = res;
    });

    var itemStatuses = Restangular.all('itemstatus');
    itemStatuses.getList().then(function(res) {
        $scope.itemStatuses = res;
    });

    var itemOwners = Restangular.all('itemowner');
    itemOwners.getList().then(function(res) {
        $scope.itemOwners = res;
    });

    var itemResponsiblePositions = Restangular.all('itemresponsibleposition');
    itemResponsiblePositions.getList().then(function(res) {
        $scope.itemResponsiblePositions = res;
    });

    var itemHomes = Restangular.all('itemhome');
    itemHomes.getList().then(function(res) {
        $scope.itemHomes = res;
    });

    $scope.edit = function() {
        $scope.edit_data = Restangular.copy($scope.data);
        $scope.edit_data.purchase_date = $filter('date')($scope.edit_data.purchase_date, "dd/MM/yyyy");
        $scope.edit_data.supplier = $scope.edit_data.supplier.url;
        $scope.edit_data.category = $scope.edit_data.category.url;
        $scope.edit_data.status = $scope.edit_data.status.url;
        $scope.edit_data.owner = $scope.edit_data.owner.url;
        $scope.edit_data.responsible_position = $scope.edit_data.responsible_position.url;
        $scope.edit_data.home = $scope.edit_data.home.url;
        $scope.editing = true;
    };

    $scope.cancelEdit = function() {
        $scope.editing = false;
    };

    function retrieveObject(list, url) {
        for (i=0; i < list.length; i++) {
            if (list[i].url == url) {
                return list[i];
            }
        }
    }

    $scope.saveEdit = function() {
        $scope.data = $scope.edit_data;
        $scope.data.purchase_date = moment($scope.data.purchase_date, "DD/MM/YYYY").format("YYYY-MM-DD");
        $scope.data.put();
        
        $scope.data.supplier = retrieveObject($scope.suppliers, $scope.data.supplier);
        $scope.data.category = retrieveObject($scope.itemCategories, $scope.data.category);
        $scope.data.status = retrieveObject($scope.itemStatuses, $scope.data.status);
        $scope.data.owner = retrieveObject($scope.itemOwners, $scope.data.owner);
        $scope.data.responsible_position = retrieveObject($scope.itemResponsiblePositions, $scope.data.responsible_position);
        $scope.data.home = retrieveObject($scope.itemHomes, $scope.data.home);

        $scope.editing = false;

    };

    $scope.addNote = function(note) {
        console.log("add called.");
        note.item = $scope.data.url;
        note.date_added = moment().format("YYYY-MM-DD");
        Restangular.all('itemnote').post(note).then(function() {
            updateNotesData();
            note.text = "";
        });
    };

});

app.controller('NoteCtrl', function($rootScope, $scope, $filter, $routeParams, $location, Restangular, $timeout) {

    $scope.editing = false;

    $scope.editNote = function (index) {
        $scope.edit_data = Restangular.copy($scope.notes[index]);
        $scope.editing = true;
    };

    $scope.cancelEditNote = function() {
        $scope.editing = false;
    };

    $scope.saveEditNote = function(index) {
        $scope.notes[index] = $scope.edit_data;
        $scope.notes[index].put();
        $scope.editing = false;
    };

});

app.controller('ItemAddCtrl', function($rootScope, $scope, Restangular, $location) {
    
    $rootScope.navName = 'additem';
    $scope.loading = true;
 
    var suppliers = Restangular.all('supplier');
    suppliers.getList().then(function(res) {
        $scope.suppliers = res;
    });

    var itemCategories = Restangular.all('itemcategory');
    itemCategories.getList().then(function(res) {
        $scope.itemCategories = res;
    });

    var itemStatuses = Restangular.all('itemstatus');
    itemStatuses.getList().then(function(res) {
        $scope.itemStatuses = res;
    });

    var itemOwners = Restangular.all('itemowner');
    itemOwners.getList().then(function(res) {
        $scope.itemOwners = res;
    });

    var itemResponsiblePositions = Restangular.all('itemresponsibleposition');
    itemResponsiblePositions.getList().then(function(res) {
        $scope.itemResponsiblePositions = res;
    });

    var itemHomes = Restangular.all('itemhome');
    itemHomes.getList().then(function(res) {
        $scope.itemHomes = res;
    });

    $scope.loading = false;

    $scope.add = function(item) {
        item.purchase_date = moment(item.purchase_date, "DD/MM/YYYY").format("YYYY-MM-DD");
        Restangular.all('item').post(item).then(function(response) {
            console.log("Saved Item");
            $location.path("/item/"+response.id);
        });
    };

});

