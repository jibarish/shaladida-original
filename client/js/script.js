var module = angular.module('app', []);

module.service('SongService', function () {
    //to create unique song id
    var uid = 1;
    
    //songs array to hold list of all songs
    var songs = [{
        id:         1,
        'title':    'Brown-Eyed Girl',
        'artist':   'Van Morrison', 
        'key':      'G', 
        'lyrics':   'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done':     true
    },
    {
        id:         2,
        'title':    'Fountain of Sorrow',
        'artist':   'Jackson Browne', 
        'key':      'G', 
        'lyrics':   'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done':     true
    }];


    
    //save method create a new song if not already exists
    //else update the existing object
    this.save = function (song) {
        if (song.id == null) {
            //if this is new song, add it in songs array
            song.id = uid++;
            songs.push(song);
        } else {
            //for existing song, find this song using id
            //and update it.
            for (i in songs) {
                if (songs[i].id == song.id) {
                    songs[i] = song;
                }
            }
        }

    }

    //simply search songs list for given id
    //and returns the song object if found
    this.get = function (id) {
        for (i in songs) {
            if (songs[i].id == id) {
                return songs[i];
            }
        }

    }
    
    //iterate through songs list and delete 
    //song if found
    this.delete = function (id) {
        for (i in songs) {
            if (songs[i].id == id) {
                songs.splice(i, 1);
            }
        }
    }

    //simply returns the songs list
    this.list = function () {
        return songs;
    }
});

module.controller('SongController', function ($scope, SongService) {

    $scope.songs = SongService.list();

    $scope.saveSong = function () {
        SongService.save($scope.newsong);
        $scope.newsong = {};
    }


    $scope.delete = function (id) {

        SongService.delete(id);
        if ($scope.newsong.id == id) $scope.newsong = {};
    }


    $scope.edit = function (id) {
        $scope.newsong = angular.copy(SongService.get(id));
    }
})