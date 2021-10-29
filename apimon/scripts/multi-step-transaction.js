(async function () {
    const assert = require("assert");
    /*
    * Test service used: https://gorest.co.in/
    * This script is a 5-step transaction.
    * Step1 - We fetch all headers from the endpoint and validate that responses are compressed.
    * Step2 - We create a user and get its id.
    * Step3 - We replace the newly created user with a new user.
    * Step4 - We update properties of the replaced user.
    * Step5 - We delete the user and validate that the status code of delete call is as expected.
    */

    // Fetch headers.
    var headers = {
        'Authorization': 'Bearer 96923d63f06237f411f84986e39cdf433820168c6ec02c7827e792c27ce0ec77'
    };
    let response = await client.head('https://gorest.co.in/public-api/users');
    assert.equal(response.headers['content-encoding'], 'gzip');

    let r = Math.random().toString(36).substring(7);

    // Create a user.
    var payload = {
        'name': `API Monitoring:${r}`,
        'gender': 'Male',
        'email': `apimonitoring${r}@synthetic.com`,
        'status': 'Active'
    };
    response = await client.post('https://gorest.co.in/public-api/users',
        {
            headers: headers,
            json: payload,
        }
    ).json();
    var id = response.data.id;

    // Replace the newly created user with a different user.
    payload = {
        'name': `API Monitoring:${r} (Added)`,
        'gender': 'Male',
        'email': `apimonitoring${r}@synthetic.com`,
        'status': 'Active'
    };
    response = await client.put(`https://gorest.co.in/public-api/users/${id}`,
        {
            headers: headers,
            json: payload
        }
    ).json();

    // Update the newly added user.
    payload = {
        'name': `API Monitoring:${r} (Updated)`,
        'gender': 'Male',
        'email': `apimonitoring${r}@synthetic.com`,
        'status': 'Active'
    };
    response = await client.patch(`https://gorest.co.in/public-api/users/${id}`,
        {
            headers: headers,
            json: payload
        }
    ).json();

    // Delete the created user.
    response = await client.delete(`https://gorest.co.in/public-api/users/${id}`,
        {
            headers: headers
        }
    ).json();

    assert.equal(response.code, 204);
})();