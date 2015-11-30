function test() {

var new_div = document.createElement('div');
new_div.id = 'block';
new_div.className = 'block';
document.getElementsByTagName('body')[0].appendChild(new_div);

var inner_div = document.createElement('div');
inner_div.className = 'block-2';

new_div.appendChild(inner_div);

}