// SPDX-License-Identifier: MIT
pragma solidity ^0.5.16;

contract FileConverter {
    mapping(uint256 => string) public fileIdToCid;
    mapping(uint256 => string) public fileIdToHashAndSignature;
    mapping(uint256 => string) public userIdToSignature;

    function storeFileIdToCid(uint256 fileId, string memory cid) public {
        fileIdToCid[fileId] = cid;
    }

    function storeFileIdToHash(uint256 fileId, string memory hash) public {
        fileIdToHashAndSignature[fileId] = hashandsignature;
    }

    function storeUserIdToSignature(uint256 userId, string memory signature) public {
        userIdToSignature[userId] = signature;
    }

    function getFileCid(uint256 fileId) public view returns (string memory) {
        return fileIdToCid[fileId];
    }

    function getFileHash(uint256 fileId) public view returns (string memory) {
        return fileIdToHashAndSignature[fileId];
    }

    function getUserSignature(uint256 userId) public view returns (string memory) {
        return userIdToSignature[userId];
    }

}
