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
	item.getList('notes').then(function(res) {
		$scope.notes = res;
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

    $scope.saveEdit = function() {
        $scope.data = $scope.edit_data;
        $scope.data.put();
        $scope.editing = false;
    };
});
app.controller('ShowingWizardCtrl', function($rootScope, $scope, Restangular, $q, $route) {
	$rootScope.navName = 'showingwizard';

	$scope.step = 1;

	var films = Restangular.all('films');
	var showings = Restangular.all('showings');
	var events = Restangular.all('events');

	var eventTypes = {};
	Restangular.one('event-types', STANDARD_EVENT_TYPE).get().then(function(res) {
		eventTypes[STANDARD_EVENT_TYPE] = res;
	});
	Restangular.one('event-types', DOUBLEBILL_EVENT_TYPE).get().then(function(res) {
		eventTypes[DOUBLEBILL_EVENT_TYPE] = res;
	});

	$scope.restart = function() {
		$route.reload();
	};

	$scope.stepOne = {
		searchFilms: function(query) {
			films.getList({search: query}).then(function(res) {
				console.log(res);
				$scope.stepOne.results = res;
			});
		},
		results: [],
		films: [],
		addFilm: function(film) {
			$scope.stepOne.films.push(Restangular.copy(film));
		},
		next: function(films) {
			$scope.stepTwo.start(films);
		}
	};
	$scope.stepTwo = {
		start: function(films) {
			if (!films.length || films.length < 1) return;
			$scope.stepTwo.films = films;
			$scope.step = 2;
		},
		back: function() {
			$scope.step = 1;
		},
		validDate: new RegExp(/^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/(19|20)\d\d$/),
		validTime: new RegExp(/^(0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])$/),
		valid: function(film) {
			if (!film) return false;
			if (!film.time || !$scope.stepTwo.validTime.test(film.time)) return false;
			return true;
		},
		formValid: function() {
			for (var i = 0; i < $scope.stepTwo.films.length; i++) {
				if (!$scope.stepTwo.valid($scope.stepTwo.films[i])) return false;
			}
			if (!$scope.stepTwo.date || !$scope.stepTwo.validDate.test($scope.stepTwo.date)) return false;
			return true;
		},
		dateValid: function(date) {
			if (!date || !$scope.stepTwo.validDate.test(date)) return false;
			return true;
		},
		films: [],
		next: function(films, date) {
			for (var i = 0; i < films.length; i++) {
				var film = films[i];
				film.moment = moment(date + " " + film.time, "DD/MM/YYYY HH:mm");
				film.datetime = film.moment.toISOString();
			}
			$scope.stepThree.start(films);
		}
	};
	$scope.stepThree = {
		start: function(films) {
			if (!films || !films.length || films.length < 1) return;
			$scope.stepThree.films = films;
			$scope.step = 3;

			// ok, now we need to build our showings and films:
			var that = $scope.stepThree;
			that.showings = [];
			that.events = [];

			// showings first:
			for (var i = 0; i < films.length; i++) {
				var showing = {
					film: films[i],
					start_time: films[i].datetime
				};
				that.showings.push(showing);
			}

			// now create events for each of those showings...
			var bigEvent = {
				name: '',
				showings: [],
				event_types: [],
				start_time: null
			};
			for (var i = 0; i < that.showings.length; i++) {
				var event = {
					name: that.showings[i].film.name,
					showings: [ that.showings[i] ],
					event_types: [ eventTypes[STANDARD_EVENT_TYPE] ],
					start_time: that.showings[i].start_time,
					ticket_types: eventTypes[STANDARD_EVENT_TYPE].ticket_templates
				};
				that.events.push(event);
				
				if (bigEvent.name != '') {
					if (i != that.showings.length - 1)
						bigEvent.name += ', ';
					else
						bigEvent.name += ' and ';
				}
				bigEvent.name += that.showings[i].film.name;
				bigEvent.showings.push(that.showings[i]);
				var thisMoment = moment(that.showings[i].start_time);
				if (bigEvent.start_time == null || thisMoment.isBefore(bigEvent.start_time)) {
					bigEvent.start_time = that.showings[i].start_time;
				}
			}

			// and one big overarching event, too
			if (that.showings.length != 1) {
				if (bigEvent.showings.length == 2) {
					bigEvent.event_types = [ eventTypes[DOUBLEBILL_EVENT_TYPE] ];
					bigEvent.ticket_types = eventTypes[DOUBLEBILL_EVENT_TYPE].ticket_templates;
				}
				that.events.push(bigEvent);
			}
		},
		back: function() {
			$scope.step = 2;
		},
		next: function() {
			if ($scope.creating) return;
			$scope.creating = true;
			// the server will attempt to help us here
			// if we generate showings, it will AUTOMATICALLY generate a corresponding "simple" event to match
			// however, any overarching events must be manually generated
			var that = $scope.stepThree;
			var promises = [];
			for (var i = 0; i < that.showings.length; i++) {
				var sshowing = that.showings[i];
				var showing = {
					'film': sshowing.film.url,
					'start_time': sshowing.start_time,
				};
				var promise = showings.post(showing);
				promise.then((function(sshowing) {
					return function(res) {
						sshowing.created = true;
						sshowing.created_obj = res;
						return res;
					};
				})(sshowing));
				promises[i] = promise;
			}

			$q.all(promises).then(function() {
				var promises = [];
				for (var i = 0; i < that.events.length; i++) {
					var sevent = that.events[i];
					if (sevent.showings.length == 1) {
						// only generate "complex" events
						sevent.created = true;
						sevent.tickets_created = true;
						continue;
					}
					var event = {
						name: sevent.name,
						start_time: sevent.start_time,
						showings: [],
						event_types: []
					};
					for (var q = 0; q < sevent.showings.length; q++) {
						event.showings.push(sevent.showings[q].created_obj.url);
					}
					for (var q = 0; q < sevent.event_types.length; q++) {
						event.event_types.push(sevent.event_types[q].url);
					}
					var promise = events.post(event);
					promise.then((function(sevent) {
						return function(res) {
							sevent.created = true;
							sevent.created_obj = res;
							res.post('reset_ticket_types_by_event_type/', {}).then(function() {
								sevent.tickets_created = true;
							});
						};
					})(sevent));
					promises.push(promise);
				}

				$q.all(promises).then(function() {
					$scope.step += 1;
				});
			});
		}
	};
});

