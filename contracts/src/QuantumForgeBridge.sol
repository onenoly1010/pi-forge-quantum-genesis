// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract QuantumForgeBridge is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;
    mapping(uint256 => string) public memorialDataRoots; // Maps TokenID -> 0G Data Root

    event MemorialResonated(uint256 indexed tokenId, address indexed pioneer, string dataRoot);

    constructor() ERC721("QuantumForgeMemorial", "QFM") Ownable(msg.sender) {}

    function mintResonatedMemorial(address pioneer, string memory tokenURI, string memory dataRoot)
        public
        onlyOwner
        returns (uint256)
    {
        uint256 tokenId = _nextTokenId++;
        _mint(pioneer, tokenId);
        _setTokenURI(tokenId, tokenURI);
        memorialDataRoots[tokenId] = dataRoot;

        emit MemorialResonated(tokenId, pioneer, dataRoot);
        return tokenId;
    }
}
