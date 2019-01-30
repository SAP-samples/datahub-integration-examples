$.setPortCallback("input",onInput);

$.setPortCallback("inResp",inResp);
var orig_resp;

function isByteArray(data) {
    switch (Object.prototype.toString.call(data)) {
        case "[object Int8Array]":
        case "[object Uint8Array]":
            return true;
        case "[object Array]":
        case "[object GoArray]":
            return data.length > 0 && typeof data[0] === 'number';
    }
    return false;
}


function inResp(ctx,s1) {
    orig_resp = s1;
}

function onInput(ctx,s) {
    var msg = {};

    var inbody = s.Body;
    var inattributes = s.Attributes;
    
    // convert the body into string if it is bytes
    if (isByteArray(inbody)) {
        inbody = String.fromCharCode.apply(null, inbody);
    }
    
    var data = inbody;
    
    //Construct response of the output from HANA client
    var resp = {};
    resp.Attributes = {};
    
    // workaround for the current limitaiton in openapi.server not deriving the content-type automatically
    resp.Attributes["openapi.header.content-type"] = "application/json";
    resp.Body = {"output": data};
    //resp.Body = {"output": "helloWorld"};
    $.sendResponse(orig_resp, resp, null);
    $.output(resp);
}

