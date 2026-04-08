//Gráfico - Gastos por Categoria
const data = window.chartData;

const labels = data.map(item => item[0]);
const values = data.map(item => item[1]);

new Chart(document.getElementById('myChart'), {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: values
        }]
    }
});

//Gráfico - Evolução Mensal
const monthly = window.monthlyData;

const labels2 = monthly.map(element => element[0]);
const values1 = monthly.map(element => element[1]);
const values2 = monthly.map(element => element[2])

new Chart(document.getElementById('monGraph'), {
    type: 'bar',
    data: {
        labels: labels2,
        datasets: [
            {
                label: 'receita',
                data: values1
            }, 
            {
                label: 'gastos',
                data: values2
            }
        ]
    }
});

//Separação de categorias pelo tipo selecionado
const typeSelect = document.getElementById('type');
const categorySelect = document.getElementById('category');

const categories = {
    expense: ["Alimentação", "Lazer", "Transporte"],
    income: ["Salário", "Renda Extra", "Investimentos"]
};

function updateCategories() {
    const selectedType = typeSelect.value;

    categorySelect.innerHTML = "";
    
    categories[selectedType].forEach(cat => {
        const option = document.createElement("option");
        option.value = cat.toLowerCase();
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
}

typeSelect.addEventListener("change", updateCategories);

updateCategories();
