const { ethers } = require("ethers");
const provider = new ethers.JsonRpcProvider("https://arb1.arbitrum.io/rpc");
const tokenAddress = "0xb0eA9F57ab3cD5B7BA90B86805B3e4B3CA0BEb98";
const walletAddress = "0xdB5247426A9Aefb98cb98B31cf936040b74b2CC4"; 

const abi = ["function balanceOf(address owner) view returns (uint256)"];
const contract = new ethers.Contract(tokenAddress, abi, provider);

contract.balanceOf(walletAddress).then(balance => {
    console.log("رصيد العملة هو:", ethers.formatUnits(balance, 18));
});
