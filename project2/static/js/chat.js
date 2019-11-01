// template for chatPost
const template = Handlebars.compile(document.querySelector('#chatPost').innerHTML);
var act_user = "";
var act_channel = "";

window.onload = function(){
    const msgArea = document.getElementById("msg");
    msgArea.addEventListener('keypress', evt => {
        if (evt.keyCode === 13 && evt.shiftKey) {
            evt.preventDefault()
            document.querySelector('#send').click();
        };
    });
;}

document.addEventListener('DOMContentLoaded', () => {
    /* connect to socket */
    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

    socket.on('connect', () => {
        document.querySelector("#send").onclick = () => {
            const msg = document.querySelector('#msg').value;
            const post_time = new Date();
            // console.log(msg);
            socket.emit('send msg', {'user': encodeURI(act_user), 'time': post_time, 
                'msg': encodeURI(msg), 'channel': encodeURI(act_channel)});
        };
    });
    
    socket.on('send username', data => {
        // console.log(JSON.stringify(data));
        act_user = decodeURI(data.act_user);
        act_channel = decodeURI(data.act_channel);
    });

    socket.on('emit msg', data => {
        const posttime = new Date(data.time);
        // console.log(JSON.stringify(data));
        const content = template(
            {'post_user': decodeURI(data.user), 'post_time': format_date(posttime), 
             'post_msg': decodeURI(data.msg), 'same_user': decodeURI(data.user)==act_user});
        document.querySelector("#msgTbl").innerHTML += content;
        document.querySelector("#msg").value = '';
        /* scroll to the page bottom */
        window.scrollTo(0, document.body.scrollHeight);
    });
});

document.addEventListener("click", evt => {
    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);
    const tgt = evt.target;
    if (tgt.dataset.class === 'del'){
        const tz_offset = new Date().getTimezoneOffset();
        const elem = tgt.parentElement.parentElement;
        const elem_user = elem.cells[0].innerText;
        const elem_time = new Date(elem.cells[1].innerText.replace(/\s/g, 'T') +
            format_tz_offset(tz_offset));
        const output = {'user': encodeURI(elem_user), 
            'time': elem_time, 'channel': encodeURI(act_channel)};
        // console.log(JSON.stringify(output));
        elem.remove();
        socket.emit("del msg", output);
    };
});

function format_chats(json_data, act_user=act_user){
    // console.log(JSON.stringify(json_data));
    var output = '';
    json_data.forEach(function(sub_json) {
        const rslt_date = new Date(sub_json[1]);
        const rslt = template({'post_user': decodeURI(sub_json[0]),
            'post_time': format_date(rslt_date), 
            'post_msg': decodeURI(sub_json[2]),
            'same_user': decodeURI(sub_json[0]) == act_user});
        output += rslt;
    });
    return output;
};

function format_date(date){
    const yr = date.getYear() + 1900;
    const mo = date.getMonth() + 1;
    const dt = date.getDate();
    const hr = date.getHours();
    const mi = date.getMinutes();
    const se = date.getSeconds(); 
    const ms = date.getMinutes();
    return yr + "-" + lead_zero(mo) + "-" + lead_zero(dt) + " " +
        lead_zero(hr) + ":" + lead_zero(mi) + ":" + lead_zero(se) + 
        "." + lead_zero(ms, 3);
};

function lead_zero(num, digits=2){
    /* put zeros in front the num */
    return (Array(digits).join(0) + num).slice(-digits);
};

function format_tz_offset(offset_min){
    const sign = (offset_min < 0) ? '+' : '-';
    const hr = Math.abs(offset_min) / 60;
    const mi = Math.abs(offset_min) % 60;
    return sign + lead_zero(hr) + ":" + lead_zero(mi);
};