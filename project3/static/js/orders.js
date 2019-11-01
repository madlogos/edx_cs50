document.addEventListener('DOMContentLoaded', () => {
    update_price();
    document.addEventListener('change', evt => {
        if(evt.target.id == 'check_all'){
            batch_check(evt.target.checked);
            update_price();
        };
        if (evt.target.dataset.class == 'order'){
            update_price();
        };
    });
    document.querySelectorAll('button').forEach(elem => {
        const btn_dict = {'btn_pay': 'pay', 'btn_cancel': 'cancel', 'btn_delete': 'delete'};
        if (['btn_pay', 'btn_cancel', 'btn_delete'].indexOf(elem.id) >= 0){
            elem.addEventListener('click', evt => {
                if (! check_clickable(btn_dict[elem.id])){
                    evt.preventDefault();
                    alert('No order is selected or \r\nnot all the selected orders can ' + btn_dict[elem.id] + '.');
                };
            });
        }else if (['pay', 'cancel', 'delete'].indexOf(elem.name) >= 0){
            elem.addEventListener('click', confirm_submit);
        };
    });
});

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});

function update_price(){
    var price = 0;
    var selected = 0;
    document.querySelectorAll('input').forEach(elem => {
        if (elem.dataset.class == 'order'){
            let item_id = elem.dataset.item;
            let item_price = Number(document.getElementById("price_" + item_id).innerHTML);
            if (elem.checked){
                selected += item_price;
            };
            price += item_price;
        };
    });
    document.getElementById("total_price").innerHTML = price.toFixed(2);
    document.getElementById("select_price").innerHTML = selected.toFixed(2);
}; 

function batch_check(check=true){
    document.querySelectorAll('input').forEach(elem => {
        if (elem.dataset.class == 'order'){
            elem.checked = check
        };
    });
};

function check_clickable(state){
    /* check if the pay_all, cancel_all, delete_all buttons are clickable */
    var o = true;
    var any_checked = false;
    const dict = {'pay': ['Pending', 'Failed'], 
                  'cancel': ['Pending', 'Failed'],
                  'delete': ['Failed', 'Cancelled']};
    document.querySelectorAll('input').forEach(elem => {
        if (elem.dataset.class == 'order'){
            if (elem.checked){
                any_checked = true;
                let item_id = elem.dataset.item;
                let item_status = document.getElementById('status_' + item_id).innerHTML;
                if (! item_status  in dict[state]){
                    o = false;
                    return false;
                };
            };
        };
    });
    if (! any_checked){
        o = false;
    };
    return o;
};

function confirm_submit(evt){
    var win = window.confirm("Confirm with the operation?");
    if (! win) {
        evt.preventDefault();
    };
};