// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 keyhash;
    event RequestedRandomness(bytes32 requestId); // Declared new type of event called RequestedRandomness

    // OPEN = 0
    // CLOSED = 1
    // CALCULATING_WINNER = 2

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // $50 minimum
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH!!!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals (en la docu de Chainlink te dice que usan 8 decimales, por lo que añadimos 10)
        // $50, $2,000 / ETH
        // 50/2,000
        // 50 * 100000 / 2000 (we multiply by some big number because Solidity has no decimals)
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice; //usdEntryFee - 18 decimals * 18 decimals que se cancelan con los 18 decimals de adjustedPrice
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        //keccack256 is a hashing algorithm
        /* uint256(
            keccack256(
                abi.encodePacked(
                    nonce, // nonce is predictable (aka transaction number)
                    msg.sender, // msg.sender is predictable
                    block.difficulty, // can actually be manipulated by the miners
                    block.timestamp // timestamp is predictable
                )
            )
        ) % players.length; 
        */
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        //Built-in function in VRFConsumerBase with request&receive. We need to have a second interaction
        bytes32 requestId = requestRandomness(keyhash, fee);

        // Built-in function in VRFConsumerBase for the receive part
        // We do it in another transaction fulfillRandomness

        // On a different note, we add the event here
        emit RequestedRandomness(requestId);
    }

    // It is internal because it will be run by the VRFCoordinator, who is the only one who should be able to run this
    // Override -- We are overriding
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You aren't there yet!!"
        );
        require(_randomness > 0, "random not found!!");

        //To pick a random player, we do modulo
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        //Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
