document.addEventListener('DOMContentLoaded', () => {
    update_price();
    document.addEventListener('change', evt => {
        if (evt.target.dataset.class == 'qty'){
            update_price();
        };
    });
    document.querySelectorAll('button').forEach(elem => {
        if (['btn_pay', 'btn_cancel', 'btn_delete'].indexOf(elem.name) >= 0){
            elem.addEventListener('click', confirm_submit);
        };
    });
});

function update_price(){
    var price = 0;
    document.querySelectorAll('input').forEach(elem => {
        if (elem.dataset.class == 'qty'){
            let item_id = elem.dataset.item;
            let unit_price = document.getElementById("product_price_" + item_id).innerHTML;
            let qty = document.getElementById('product_' + item_id).value;
            let item_price = Number(qty) * Number(unit_price);
            
            price += item_price;
        };
    });
    document.getElementById("total_price").innerHTML = price.toFixed(2);
}; 

function confirm_submit(evt){
    var win = window.confirm("Confirm with the operation?");
    if (! win) {
        evt.preventDefault();
    };
};