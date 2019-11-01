document.addEventListener('DOMContentLoaded', () => {
    const submit = document.querySelector('#btn_submit');
    const n_topping = document.getElementById('n_topping');
    const qty_limit = (n_topping == null) ? null : Number(n_topping.innerHTML);

    submit.addEventListener('click', evt => {
        if (! check_toppings(qty_limit)){
            evt.preventDefault();
            alert("Please select exactly " + qty_limit + " toppings.");
        }else{
            document.forms['prod_form'].submit();
        };
    });

    document.addEventListener('change', evt => {
        if (evt.target.dataset.class == 'topping' || evt.target.dataset.class == 'addition'){
            update_price();
        };
    });
});


function check_toppings(limit){
    var qty = 0;
    if (limit == null){
        return true;
    };
    document.querySelectorAll('input').forEach(elem => {
        if (elem.dataset.class == 'topping'){
            qty += Number(elem.value);
        };
    });
    return qty == limit;
};

function update_price(){
    var price = Number(document.getElementById("price").innerHTML);
    document.querySelectorAll('input').forEach(elem => {
        if (elem.dataset.class == 'topping' || elem.dataset.class == 'addition'){
            let add_price = document.getElementById(elem.dataset.class + "_price_" + elem.dataset.item).innerHTML;
            price += Number(elem.value) * Number(add_price);
        };
    });
    document.getElementById("price").innerHTML = price.toFixed(2);
}; 