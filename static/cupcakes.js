const BASE_URL = "http://localhost:5000/api";

$("form").on("submit", createCupcake);

async function createCupcake(evt) {
    evt.preventDefault();
    const flavor = $("#flavor").val();
    const rating = $("#rating").val();
    const size = $("#size").val();
    const image = $("#image").val();
    let data = {
        flavor,
        rating,
        size,
        image,
    };

    await axios.post(`${BASE_URL}/cupcakes`, data);
    displayAllCupcakes();
}

async function displayAllCupcakes() {
    const res = await axios.get(`${BASE_URL}/cupcakes`);
    const ul = $("#cupcakesList");

    // empty out the <ul> first to start clean
    ul.empty();

    for (let cupcake of res.data.cupcakes) {
        let li = `<li>${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}</li>`;
        ul.append(li);
    }
}

displayAllCupcakes();
