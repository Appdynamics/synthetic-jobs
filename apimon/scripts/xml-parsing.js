// Javascript based API Monitoring Test

const assert = require("assert");
const xml2js = require('xml2js');
(async () => {
    var url = "https://www.w3schools.com/xml/plant_catalog.xml";
    var response = await client.get(url);
    var data = response.body;
    assert.equal(200, response.statusCode);
    xml2js.parseString(data, function(err, result) {
        console.log(result);
    });
})();