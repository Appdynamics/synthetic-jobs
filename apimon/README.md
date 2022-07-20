## Synthetics API Monitoring (APIMon)

Synthetic API Monitoring feature enables monitoring of HTTP(s) based APIs (internal, external and third party) from different geo locations across the world and provides visibility into :
  - Uptime/Availability of api
  - Performance of api
  - Correctness of api

### API Monitoring Usage
Scheduling of API Monitoring Jobs is the same as Web Monitoring. The major difference in API Monitoring is the scripting language. Here, we will discuss how to write scripts for API Monitoring. 
API Monitoring uses JavaScript as the scripting language and got client library ( https://github.com/sindresorhus/got ) for making requests. It is recommended to check out the documentation on its Github Page.

While writing the scripts in the job editor, customer does not have to import got library. The Script already has a client object injected into the sample script and only the requests made using this client 
object will be captured by the session.


#### Making Requests
The client returns a promise which will resolve to a response object. You can either use it as a promise or with async / await. 

##### Using with Async / Await

```javascript
   (async () => {
        // GET Request
        var response = await client.get("https://www.google.com/");
        console.log(response.statusCode); // 200
        console.log(response.statusMessage); // OK
        console.log(response.body); // HTML Body
     
        // POST, PUT or DELETE Request
         response = await client.post("https://www.google.com/");   
         response = await client.put("https://www.google.com/");
         response = await client.delete("https://www.google.com/");
      })(); // Make sure to call the async function at the end 
      //Using with Promises
      // GET Request
       client.get("https://www.google.com/").then(response => {
       console.log(response.statusCode); // 200
       console.log(response.statusMessage); // OK
       console.log(response.body); // HTML Body
    });

    // POST, PUT, DELETE Request
    client.post("https://www.google.com/");
    client.put("https://www.google.com/");
    client.delete("https://www.google.com/");
``` 

We can make GET, POST, PUT or DELETE request using the client object.
From here on, we will use async/await to showcase other features but all those can also be used with promises.

#### Sending Custom Headers and Query Parameters 
The second argument to any of the methods on the client object takes options for everything. You can add your headers and query params using those options.

##### Headers and Query Params

```javascript
(async () => {
    var response = await client.get("https://www.google.com/", {
                        headers : { "X-Custom-Header" : "Custom-Header-Value" },
                    })
    var response = await client.get("https://www.google.com/", {
                        searchParams : { "param" : "value" }, // Will make the request to "https://www.google.com/?param=value"
                    })
})();

```
 
#### Sending Request Body
There are three ways to send body.
Using 'body' option which expects the string or Buffer or stream.Readable.
Using 'json' option which expects a JSON serializable object and it will set the "Content-Type" header "application/json".
Using 'form' which expects an object and coverts it to  a query string using "(new URLSearchParams(object)).toString()" sets the "Content-Type" header "application/x-www-form-urlencoded".

```javascript
(async () => {
    var response = await client.post("http://www.google.com/", { body: "Raw Body" }); // Body : 'Raw Body'
    var response = await client.post("http://www.google.com/", {
                        json: { name : "John Doe", age : 25 }       // Body : '{ "name":"John Doe", "age": 25}'
                    });
    var response = await client.post("http://www.google.com/", {
                        form: { name : "John Doe", age : 25 }       // Body : 'name=John+Doe&age=25'
                    });
})();
Parsing Response
For headers, use response.headers and for body, use response.body.
(async () => {
    var response = await client.post("http://www.google.com/");
    console.log(response.headers); // List of headers
    console.log(response.body); // Response Body
})();
```

You can also parse the response body automatically by using the ".json()" function or setting the "responseType" option to "json". 
The "responseType" option can be set to either "text", "json" or "buffer".
Note that, ".json()" function can only be used on the promise directly and not on the response object and it will return the parsed response body and will not retain headers and other data. If you want to keep the headers and other metadata, then you should use the option "responseType" set to "json".

```javascript
(async () => {
    var body = await client.post("https://randomuser.me/api/").json();
    console.log(body); // JSON Parsed Response Body
     
    var response = await client.post("https://randomuser.me/api/", {responseType: "json");
    console.log(response.body); // JSON Parsed Response Body
 
 
    var body = await client.post("https://randomuser.me/api/").buffer();
    console.log(body); // Response Body Buffer
     
    var response = await client.post("https://randomuser.me/api/", {responseType: "buffer");
    console.log(response.body); // Response Body Buffer
 
})();
```

#### Parsing XML
API Monitoring has a library called "xml2js" which can be used to parse the XML Data.

##### XML Parsing
```javascript
const assert = require("assert");
const xml2js = require('xml2js');
(async () => {
    var url = "<% SOME XML URL %>";
    var response = await client.get(url);
    var data = response.body;
    xml2js.parseString(data, function(err, result) {
        console.log(result);
    });
})();
Read more about this library here : https://www.npmjs.com/package/xml2js
Adding Assertions
To use assertions, you'll need to import the assert module and use it as you would for any script.
const assert = require("assert");
(async () => {
    var response = await client.get("https://test.requestcatcher.com/test");
 
    assert.equal(200, response.statusCode);
    assert.equal("request caught", response.body);
 
    assert.strict.strictEqual(200, response.statusCode);
    assert.strict.strictEqual("request caught", response.body);
 
    assert.notEqual(500, response.statusCode);
})();
```


#### Encryption
You might need to encrypt/decrypt payloads, create digital signatures, verify integrity of data, etc as part of your API Monitoring tests. We've a couple of libraries included for the encryption needs.
- [jose](https://github.com/panva/jose) - provides support for Universal "JSON Web Almost Everything" - JWA, JWS, JWE, JWT, JWK.
- [xml-crypto](https://github.com/yaronn/xml-crypto) - An XML digital signature library.
- [xmldom](https://github.com/xmldom/xmldom) - DOM parser to be used along with xml-crypto for verifying XML Documents.
- [crypto](https://nodejs.org/api/crypto.html) - The Node.js's crypto module provides cryptographic functionality that includes a set of wrappers for OpenSSL's hash, HMAC, cipher, decipher, sign, and verify functions.
##### Example usage:

##### JWE Encryption & Decryption

```javascript
(async () => {
    const { CompactEncrypt } = require('jose/jwe/compact/encrypt')
    const { compactDecrypt } = require('jose/jwe/compact/decrypt')
  
    const encoder = new TextEncoder()
  
    // The payload for JWE
    const payload = {
        text: "Hello World!"
    }
  
    // Secret key for A128GCM
    const secretKey = encoder.encode("asecret128bitkey")
  
    // Generating the JWE Token
    const jweToken = await new CompactEncrypt(encoder.encode(JSON.stringify(payload)))
        .setProtectedHeader({ alg: 'dir', enc: 'A128GCM' })
        .encrypt(secretKey)
  
    console.log(jweToken)
  
    // Decrypting the JWE token to get protected headers and the payload
    const decoder = new TextDecoder()
    const { plaintext, protectedHeader } = await compactDecrypt(jweToken, secretKey)
  
    console.log(protectedHeader)
    console.log(decoder.decode(plaintext))
  
})()
```

##### XML Signing & Verification

```javascript
(async () => {
    const select = require('xml-crypto').xpath,
        dom = require('@xmldom/xmldom').DOMParser,
        SignedXml = require('xml-crypto').SignedXml,
        FileKeyInfo = require('xml-crypto').FileKeyInfo,
        fs = require('fs'),
        crypto = require('crypto')
 
    cert_str = "-----BEGIN CERTIFICATE-----<REDACTED>-----END CERTIFICATE-----\n"
    key_str = "-----BEGIN RSA PRIVATE KEY-----<REDACTED>-----END RSA PRIVATE KEY-----\n"
    auth_data_to_sign = '<?xml version="1.0" encoding="UTF-8"?><oAuthToken xmlns="http://com.citi.citiconnect/services/types/oauthtoken/v1"><grantType>client_credentials</grantType><scope>/authenticationservices/v1</scope><sourceApplication>CCF</sourceApplication></oAuthToken>'
    keyPassphrase="<REDACTED>"
 
    /*
     * xml-crypto cannot directly deal with private keys that are encrypted with a passphrase.
     * For that, we'll first need to decrypt the private key and then pass the
     * decrypted key to xml-crypto for signing the XML document
     */
    const encryptedKey = crypto.createPrivateKey({
        key: key_str,
        passphrase: keyPassphrase
    })
 
    const decryptedKey = encryptedKey.export({
        format: 'pem',
        type: 'pkcs1',
    })
 
    const decryptedKeyBuffer = Buffer.from(decryptedKey)
 
    // Computing the signature
    const sig = new SignedXml()
    sig.addReference(
        // reference to the root node
        "/*",
        [
            'http://www.w3.org/2000/09/xmldsig#enveloped-signature',
            'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
        ],
        'http://www.w3.org/2000/09/xmldsig#sha1',
        '',
        '',
        '',
        // let the URI attribute with an empty value,
        // this is the signal that the signature is affecting the whole xml document
        true
    );
 
    /*
     * For a list of supported Signature Algorithms, Hashing Algorithms, Canonicalization and Transformation Algorithms
     * go through the documentation of xml-crypto on GitHub here: https://github.com/yaronn/xml-crypto
     */
    sig.signingKey = decryptedKeyBuffer
    sig.canonicalizationAlgorithm = 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
    sig.computeSignature(auth_data_to_sign)
 
    // Write the signed xml to a file named 'signed.xml'
    fs.writeFileSync("signed.xml", sig.getSignedXml());
 
    // Verifying the XML signature of the file 'signed.xml'
    (() => {
        const xml = fs.readFileSync("signed.xml").toString()
        const doc = new dom().parseFromString(xml)
 
        const signature = select(doc, "//*[local-name(.)='Signature' and namespace-uri(.)='http://www.w3.org/2000/09/xmldsig#']")[0]
        const sig = new SignedXml()
        fs.writeFileSync("client_public.pem", cert_str)
        sig.keyInfoProvider = new FileKeyInfo("client_public.pem")
        sig.loadSignature(signature)
        const res = sig.checkSignature(xml)
        if (!res) console.log(sig.validationErrors)
    })()
 
})()
```

For more examples and detailed documentation on the capabilities of these libraries, visit their respective GitHub repos.

##### Conclusion
This document covers the major use cases but it is still recommended to read the got client documentation ( https://github.com/sindresorhus/got ). 


