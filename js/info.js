/* =========================================
   GEEKWAVE PRODUCT DETAIL
   ========================================= */

const productData = {
    flavors: {
        black: {
            name: "Chasis Black",
            icon: "",
            main: "https://res.cloudinary.com/dn8pns203/image/upload/v1777401872/geekwave_catalog/vybuwhqgbpi4hi4nxom4.webp",
            gallery: [
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401872/geekwave_catalog/vybuwhqgbpi4hi4nxom4.webp",
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401873/geekwave_catalog/hkh80zcxx5hci35cxxhm.webp",
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401874/geekwave_catalog/cq6hbuxovqkfm3zuwnfn.webp"
            ],
            description:
                "El estándar de ingeniería. Un acabado negro mate texturizado que evoca la estética clásica."
        },

        white: {
            name: "Chasis White",
            icon: "",
            main: "https://res.cloudinary.com/dn8pns203/image/upload/v1777401874/geekwave_catalog/ywos3mcw8lwsv4aghdku.webp",
            gallery: [
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401874/geekwave_catalog/ywos3mcw8lwsv4aghdku.webp",
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401875/geekwave_catalog/l9roi8hkdwqztfbbdurm.webp",
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401875/geekwave_catalog/nd9yy2izwhplgli7avxo.webp",
                "https://res.cloudinary.com/dn8pns203/image/upload/v1777401876/geekwave_catalog/xejjdgcatgzvd9a7k2qp.webp"
            ],
            description:
                "Minimalismo técnico. La versión White destaca la pureza visual del sistema."
        }
    },

    plans: {
        standard: {
            buttonText: "RESERVAR EDICIÓN BASE",
            benefits: [
                "Consola Analogue Pocket Original",
                "Cable USB-C",
                "Protector de pantalla"
            ]
        },

        bundle: {
            buttonText: "RESERVAR DELUXE BUNDLE",
            benefits: [
                "Consola Analogue Pocket",
                "Analogue Dock",
                "Hard Case",
                "Envío prioritario"
            ]
        }
    }
};

let selectedFlavor = "black";
let selectedPlan = "standard";
let quantity = 1;
let productoActual = null;

/* =========================================
   GALLERY + FLAVORS
   ========================================= */

function renderSelectors() {

    const flavorContainer =
        document.getElementById("flavorContainer");

    const galleryThumbs =
        document.getElementById("galleryThumbs");

    const mainImage =
        document.getElementById("mainProductImage");

    if (!flavorContainer || !galleryThumbs || !mainImage)
        return;

    flavorContainer.innerHTML = "";
    galleryThumbs.innerHTML = "";

    const currentFlavor =
        productData.flavors[selectedFlavor];

    Object.entries(productData.flavors)
        .forEach(([key, flavor]) => {

            const button =
                document.createElement("button");

            button.className =
                `flavor-btn ${
                    selectedFlavor === key
                        ? "active"
                        : ""
                }`;

            button.innerHTML =
                `<span>${flavor.name}</span>`;

            button.addEventListener("click", () => {

                selectedFlavor = key;

                updateUI();

            });

            flavorContainer.appendChild(button);

        });

    currentFlavor.gallery.forEach((imgUrl, index) => {

        const thumb =
            document.createElement("div");

        thumb.className =
            `thumb ${index === 0 ? "active" : ""}`;

        thumb.innerHTML =
            `<img src="${imgUrl}" alt="">`;

        thumb.addEventListener("click", () => {

            mainImage.src = imgUrl;

            document
                .querySelectorAll(".thumb")
                .forEach(t =>
                    t.classList.remove("active")
                );

            thumb.classList.add("active");

        });

        galleryThumbs.appendChild(thumb);

    });

}

/* =========================================
   PLAN DETAILS
   ========================================= */

function renderPlanDetails() {

    const plan =
        productData.plans[selectedPlan];

    const benefitsList =
        document.getElementById("benefitsList");

    const cartButton =
        document.getElementById("cartButton");

    if (benefitsList) {

        benefitsList.innerHTML =
            plan.benefits
                .map(item => `
                    <li>
                        <i class="fa-solid fa-circle-check"></i>
                        ${item}
                    </li>
                `)
                .join("");

    }

    if (cartButton) {

        cartButton.innerHTML = `
            ${plan.buttonText}
            <i class="fa-solid fa-chevron-right"></i>
        `;

    }

}

/* =========================================
   MAIN UI UPDATE
   ========================================= */

function updateUI() {

    const flavor =
        productData.flavors[selectedFlavor];

    const mainImage =
        document.getElementById("mainProductImage");

    const description =
        document.getElementById("productDescription");

    if (mainImage) {

        mainImage.src = flavor.main;

    }

    if (description) {

        description.style.opacity = 0;

        setTimeout(() => {

            description.textContent =
                flavor.description;

            description.style.opacity = 1;

        }, 150);

    }

    renderSelectors();
    renderPlanDetails();

}

/* =========================================
   QUANTITY
   ========================================= */

function setupQuantityControls() {

    const increaseBtn =
        document.getElementById("increaseQty");

    const decreaseBtn =
        document.getElementById("decreaseQty");

    const quantityValue =
        document.getElementById("quantityValue");

    if (!increaseBtn || !decreaseBtn || !quantityValue)
        return;

    increaseBtn.addEventListener("click", () => {

        quantity++;

        quantityValue.textContent =
            quantity;

    });

    decreaseBtn.addEventListener("click", () => {

        if (quantity > 1) {

            quantity--;

            quantityValue.textContent =
                quantity;

        }

    });

}

/* =========================================
   PLAN SELECTORS
   ========================================= */

function setupPlanSelectors() {

    document
        .querySelectorAll(".config-option")
        .forEach(btn => {

            btn.addEventListener("click", () => {

                document
                    .querySelectorAll(".config-option")
                    .forEach(b =>
                        b.classList.remove("active")
                    );

                btn.classList.add("active");

                selectedPlan =
                    btn.dataset.plan;

                renderPlanDetails();

            });

        });

}

/* =========================================
   ACCORDIONS
   ========================================= */

function setupAccordions() {

    document
        .querySelectorAll(".accordion-header")
        .forEach(header => {

            header.addEventListener(
                "click",
                () => {

                    const item =
                        header.parentElement;

                    item.classList.toggle("active");

                    const icon =
                        header.querySelector("i");

                    if (icon) {

                        icon.classList.toggle("fa-plus");
                        icon.classList.toggle("fa-minus");

                    }

                }
            );

        });

}

/* =========================================
   LOAD PRODUCT
   ========================================= */

async function loadProduct() {

    try {

        const params =
            new URLSearchParams(
                window.location.search
            );

        const productId =
            params.get("id");

        if (!productId)
            return;

        const response =
            await fetch(
                "json/inventario.json"
            );

        const inventario =
            await response.json();

        const producto =
            inventario.find(
                p =>
                    String(p.id) ===
                    String(productId)
            );

        if (!producto)
            return;

        productoActual = producto;

        const title =
            document.getElementById(
                "productTitle"
            );

        if (title) {

            title.textContent =
                producto.nombre;

        }

        const desc =
            document.getElementById(
                "productDescription"
            );

        if (desc &&
            producto.descripcion_tecnica) {

            desc.textContent =
                producto.descripcion_tecnica;

        }

        const basePrice =
            document.getElementById(
                "basePrice"
            );

        if (basePrice) {

            basePrice.textContent =
                `$${producto.precio_usd}`;

        }

        const bundlePrice =
            document.getElementById(
                "bundlePrice"
            );

        if (bundlePrice) {

            bundlePrice.textContent =
                `$${(
                    Number(producto.precio_usd) + 50
                ).toFixed(2)}`;

        }

    } catch (error) {

        console.error(
            "Error cargando producto:",
            error
        );

    }

}

/* =========================================
   CART
   ========================================= */

function setupCartButton() {

    const cartButton =
        document.getElementById(
            "cartButton"
        );

    if (!cartButton)
        return;

    cartButton.addEventListener(
        "click",
        () => {

            if (!productoActual)
                return;

            if (
                typeof window.addToCart ===
                "function"
            ) {

                window.addToCart(
                    productoActual.id,
                    productoActual.nombre,
                    quantity
                );

            }

        }
    );

}

/* =========================================
   INIT
   ========================================= */

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        setupQuantityControls();

        setupPlanSelectors();

        setupAccordions();

        setupCartButton();

        await loadProduct();

        updateUI();

    }
);