$.setPortCallback("input",onInput);

//Checks the data if in bytes
//Incase of bytes we need to convert to string
function isByteArray(data) {
    return (typeof data === 'object' && Array.isArray(data) 
        && data.length > 0 && typeof data[0] === 'number')
}

function onInput(ctx,s) {
    var msg = {};
    var inbody = s.Body;
    var inattributes = s.Attributes;
    
    // convert the body into string if it is bytes
    if (isByteArray(inbody)) {
        inbody = String.fromCharCode.apply(null, inbody);
    }

    // just send a copy of the request to the output for someone else (e.g., if port output is connected)
    msg.Attributes = {};
    for (var key in inattributes) {
        msg.Attributes[key] = inattributes[key];
    }
    msg.Body = inbody;
    

    // pass a copy to the output if connected
    if ($.output != null) {
        $.output(s);
    }
    
    //Construct message SQL (Just the holder)
    var msgSQL = {};
    msgSQL.Body = {};
    
    // send the response
    var reqmethod = inattributes["openapi.method"];
    var reqpath = inattributes["openapi.request_uri"];
    var opid = inattributes["openapi.operation_id"];
    var tabName = inattributes["openapi.path_params.hanaTable"];
    
    //Construct response holder
    var resp = {};
    resp.Attributes = {};
    
    // workaround for the current limitaiton in openapi.server not deriving the content-type automatically
    resp.Attributes["openapi.header.content-type"] = "application/json";
    
    switch (opid) {
        case "getDummy":
            var str = "select * from dummy;";
            msgSQL.Body = str;
            $.outsql(msgSQL);
            break;
        case "getHanaTable":
            var str = "select * from " + tabName + ";";
            msgSQL.Body = str;
            $.outsql(msgSQL);
            break;
        default:
            $.sendResponse(s, null, Error("Unexpected operation ID " + opid))
            break;
    }
}

