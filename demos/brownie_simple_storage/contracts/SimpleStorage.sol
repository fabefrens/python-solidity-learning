//SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    // this will get initialized to zero
    uint256 favoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    // Structs -- Arbitrary data type
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //Arrays
    People[] public people;
    People[1] public fixedArrayPeople;

    //Mappings
    mapping(string => uint256) public nameToFavoriteNumber;

    // Public vs internal vs external vs private
    People public person = People({favoriteNumber: 2, name: "Carlos"});

    // view -- only reading state of the blockchain
    // technically variables are view functions
    // pure -- They do pure math (e.g. favoriteNumber*2)ç
    // view, pure, they don't change the state of the blockchain
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function retrieve2(uint256 _favoriteNumber) public pure {
        _favoriteNumber + _favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
