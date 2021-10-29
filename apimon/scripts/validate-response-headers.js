(async function() {
    const assert = require("assert");
    /*
    * Test service used: https://gorest.co.in/
    * This script creates a new user and then validates its headers.
    * We can check for equality as well as for substrings.
    */

    // Create a new user.
    var headers = {
        'Authorization': 'Bearer 96923d63f06237f411f84986e39cdf433820168c6ec02c7827e792c27ce0ec77'
    };
    var payload = {
        'name': 'Natasha Romanov',
        'gender': 'Female',
        'email': 'nat50@marvel.com',
        'status': 'Active'
    };

    // To obtain headers, DON'T resolve with json() or text().
    var response = await client.post('https://gorest.co.in/public-api/users',
        {
            headers: headers,
            json: payload
        }
    );

    assert.equal(response.headers['content-encoding'], 'gzip');
})();