pragma solidity ^0.4.0;

contract App {

    mapping(bytes24 => string) public app;

    function App() public{
        app["Vote"] = "QmWvMxzFoKjUh4nF9Knf5XSYguVgzArzVZcsNXUJComLvD";
    }

    function setNode(bytes24 appName, string Ohash){
	app[appName] = Ohash;
    }

    function GetOhash(bytes24 appName) constant returns (string) {
        return app[appName];
    }

}
