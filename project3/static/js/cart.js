document.addEventListener('DOMContentLoaded', () => {
    update_price();
    document.addEventListener('change', evt => {
        if (evt.target.id == 'check_all'){
            batch_check(evt.target.checked);
            update_price();
        };
        if (evt.target.dataset.class == 'qty' || evt.target.dataset.class == 'order'){
            update_price();
        };
    });
    document.getElementById('btn_submit').addEventListener('click', evt => {
        let select = document.getElementById('select_price').innerHTML;
        if (Number(select) == 0){
            evt.preventDefault();
            alert("Please select at least 1 item."); 
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
        if (elem.dataset.class == 'qty' || elem.dataset.class == 'order'){
            let item_id = elem.dataset.item;
            let unit_price = document.getElementById("product_price_" + item_id).innerHTML;
            let qty = document.getElementById('product_' + item_id).value;
            let item_price = Number(qty) * Number(unit_price);
            
            if (elem.dataset.class == 'order'){
                if (elem.checked){
                    selected += item_price;
                };
            }else{
                price += item_price;
            };
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