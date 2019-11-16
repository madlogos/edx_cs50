// template for chatPost
const template = Handlebars.compile(document.querySelector('#chatPost').innerHTML);

window.onload = function(){
    const msgArea = document.getElementById("msg");
    msgArea.addEventListener('keypress', evt => {
        if (evt.keyCode === 13 && evt.shiftKey) {
            evt.preventDefault()
            document.querySelector('#send').click();
        };
    });
};

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

    socket.on('emit msg', data => {
        console.log('emit msg: ' + JSON.stringify(data));
        if (act_channel == data.channel){
            const posttime = new Date(data.time);
            const content = template(
                {'post_id': data.id, 'post_user': decodeURI(data.user), 'post_time': format_date(posttime), 
                 'post_msg': decodeURI(data.msg), 'same_user': decodeURI(data.user)==act_user});
            document.querySelector("#msgTbl").innerHTML += content;
            document.querySelector("#msg").value = '';
            /* scroll to the page bottom */
            window.scrollTo(0, document.body.scrollHeight);
        };
    });
});

document.addEventListener("click", evt => {
    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);
    const tgt = evt.target;
    if (tgt.dataset.class === 'del'){
        const elem = tgt.parentElement.parentElement;
        elem.remove();
        console.log(encodeURI(act_channel) + ': ' + tgt.dataset.id);
        socket.emit("del msg", {'channel': encodeURI(act_channel), 'id': tgt.dataset.id});
    };
});

function format_chats(json_data, act_user=act_user){
    console.log(JSON.stringify(json_data)); 
    /* json_data is a dict */
    var output = '';
    Object.keys(json_data).forEach(function(key) {
        const rslt_date = new Date(json_data[key]['time']);
        const rslt = template({
            'post_id': key,
            'post_user': decodeURI(json_data[key]['user']),
            'post_time': format_date(rslt_date), 
            'post_msg': decodeURI(json_data[key]['msg']),
            'same_user': decodeURI(json_data[key]['user']) == act_user});
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

// function format_tz_offset(offset_min){
//     const sign = (offset_min < 0) ? '+' : '-';
//     const hr = Math.abs(offset_min) / 60;
//     const mi = Math.abs(offset_min) % 60;
//     return sign + lead_zero(hr) + ":" + lead_zero(mi);
// };