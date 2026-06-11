// check_contract_logic.js
const { ethers } = require("ethers");
const provider = new ethers.JsonRpcProvider("https://arb1.arbitrum.io/rpc");
const address = "0xb0eA9F57ab3cD5B7BA90B86805B3e4B3CA0BEb98";

async function test() {
    try {
        const code = await provider.getCode(address);
        if (code === "0x") {
            console.log("خطأ: العنوان ليس عقداً ذكياً!");
        } else {
            console.log("العقد موجود ومفعل. الكود البرمجي تم سحبه بنجاح.");
        }
    } catch (e) {
        console.log("فشل الاتصال:", e.message);
    }
}
test();
