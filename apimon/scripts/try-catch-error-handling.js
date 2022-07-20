// Javascript based API Monitoring Test

const assert = require("assert");
(async () => {
    try {
        var x = Math.floor((Math.random() * 10) + 1) % 2;
        var response;
        if(x === 0) {
            response = await client.get("http://httpstat.us/500");
            assert.equal(response.statusCode, 500);
            throw "Internal Server Error"
        } else {
            response = await client.get("http://httpstat.us/200");
        }
        assert.equal(response.statusCode, 200);
        assert.equal(response.statusMessage, "OK");
        for(var key in response.headers) {
            console.log(`${key} : ${response.headers[key]}`);
        }
    }
    catch (err) {
        console.log(err);
    }
})()