const assert = require("assert");
(async function () {
    let response = await client.get('https://postman-echo.com/get?foo1=bar1&foo2=bar2');
    console.log(response.body);
    let jsonResponse = JSON.parse(response.body);
    assert.equal(response.statusCode, 200);
    assert.equal(jsonResponse.args.foo1, "bar1");
})();