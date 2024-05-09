var pickles = 0;
var pps = 0;
var Version_name = "Unicorn_0.0.1"

cost_pickle_farmer = 100
cost_pickle_factory = 1337
cost_pickle_plane = 11111

pps_pickle_farmer = 1
pps_pickle_factory = 10
pps_pickle_plane = 101

amount_pickle_farmer = 0
amount_pickle_factory = 0
amount_pickle_plane = 0

if (save_data[1] !== undefined) {
    Version_name = save_data[0]
    pickles = save_data[1]
    pps = save_data[2]

    amount_pickle_farmer = save_data[3]
    amount_pickle_factory = save_data[4]
    amount_pickle_plane = save_data[5]

    cost_pickle_farmer = save_data[6]
    cost_pickle_factory = save_data[7]
    cost_pickle_plane = save_data[8]
}
function make_Download_Request() {
    document.querySelector('input[name=version_name]').value = Version_name
    document.querySelector('input[name=pickle_amount]').value = pickles
    document.querySelector('input[name=pps_amount]').value = pps
    document.querySelector('input[name=amount_pickle_farmer]').value = amount_pickle_farmer
    document.querySelector('input[name=amount_pickle_factory]').value = amount_pickle_factory
    document.querySelector('input[name=amount_pickle_plane]').value = amount_pickle_plane
    document.querySelector('input[name=cost_pickle_farmer]').value = cost_pickle_farmer
    document.querySelector('input[name=cost_pickle_factory]').value = cost_pickle_factory
    document.querySelector('input[name=cost_pickle_plane]').value = cost_pickle_plane

    return true
}

function increase_price(old_price) {
    return Math.round(old_price * 1.15)
}
function pickle_click() {
    pickles++;
    document.getElementById('pickles').innerHTML = "Pickles: " + pickles;
}


function buy_pickle_farmer() {
    if (pickles >= cost_pickle_farmer) {
        pps += pps_pickle_farmer
        pickles -= cost_pickle_farmer
        amount_pickle_farmer += 1
        cost_pickle_farmer = increase_price(cost_pickle_farmer)
    }

    document.getElementById('pps').innerHTML = "PPS: " + pps;
}
function buy_pickle_factory() {
    if (pickles >= cost_pickle_factory) {
        pps += pps_pickle_factory
        pickles -= cost_pickle_factory
        amount_pickle_factory += 1
        cost_pickle_factory = increase_price(cost_pickle_factory)
    }

    document.getElementById('pps').innerHTML = "PPS: " + pps;
}

function buy_pickle_plane() {
    if (pickles >= cost_pickle_plane) {
        pps += pps_pickle_plane
        pickles -= cost_pickle_plane
        amount_pickle_plane += 1
        cost_pickle_plane = increase_price(cost_pickle_plane)
    }

    document.getElementById('pps').innerHTML = "PPS: " + pps;
}



function update() {
    document.getElementById('version').innerHTML                = "Version: "           + Version_name;
    document.getElementById('pickles').innerHTML                = "Pickles: "           + pickles;
    document.getElementById('pps').innerHTML                    = "PPS: "               + pps;
    document.getElementById('pickle_farmer_cost').innerHTML     = "Cost: "              + cost_pickle_farmer;
    document.getElementById('pickle_factory_cost').innerHTML    = "Cost: "              + cost_pickle_factory;
    document.getElementById('pickle_plane_cost').innerHTML      = "Cost: "              + cost_pickle_plane;
    document.getElementById('pickle_farmer_amount').innerHTML   = "Farmer amount: "     + amount_pickle_farmer;
    document.getElementById('pickle_factory_amount').innerHTML  = "Factory amount: "    + amount_pickle_factory;
    document.getElementById('pickle_plane_amount').innerHTML    = "Plane amount: "      + amount_pickle_plane;
}

window.setInterval(
    function () {
        pickles = pickles + pps/10
        pickles = Math.round(pickles*100)/100;

        update()

    }, 100);