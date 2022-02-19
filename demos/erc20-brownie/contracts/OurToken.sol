// contracts/OurToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OurToken is ERC20 {
    constructor(
        uint256 initialSupply,
        string memory token_name,
        string memory token_symbol
    ) ERC20(token_name, token_symbol) {
        _mint(msg.sender, initialSupply);
    }
}
