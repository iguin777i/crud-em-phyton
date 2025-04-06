let pneuModal;
let pneus = [];

document.addEventListener('DOMContentLoaded', () => {
    pneuModal = new bootstrap.Modal(document.getElementById('pneuModal'));
    loadPneus();
    
    document.getElementById('searchInput').addEventListener('input', (e) => {
        searchPneus(e.target.value);
    });
});

async function loadPneus() {
    try {
        const response = await fetch('/api/pneus');
        pneus = await response.json();
        renderPneus(pneus);
    } catch (error) {
        console.error('Erro ao carregar pneus:', error);
    }
}

function renderPneus(pneusToRender) {
    const tbody = document.getElementById('pneusTableBody');
    tbody.innerHTML = '';
    
    pneusToRender.forEach(pneu => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${pneu.dimensoes}</td>
            <td>${pneu.marca}</td>
            <td>${pneu.tipo}</td>
            <td>${pneu.quantidade}</td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-info" onclick="editPneu(${pneu.id})">Editar</button>
                <button class="btn btn-sm btn-danger" onclick="deletePneu(${pneu.id})">Excluir</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function searchPneus(query) {
    try {
        const response = await fetch(`/api/pneus/buscar?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        renderPneus(results);
    } catch (error) {
        console.error('Erro ao buscar pneus:', error);
    }
}

function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Adicionar Pneu';
    document.getElementById('pneuForm').reset();
    document.getElementById('pneuId').value = '';
    pneuModal.show();
}

async function editPneu(id) {
    const pneu = pneus.find(p => p.id === id);
    if (!pneu) return;
    
    document.getElementById('modalTitle').textContent = 'Editar Pneu';
    document.getElementById('pneuId').value = pneu.id;
    document.getElementById('dimensoes').value = pneu.dimensoes;
    document.getElementById('indice_carga').value = pneu.indice_carga;
    document.getElementById('indice_velocidade').value = pneu.indice_velocidade;
    document.getElementById('tipo').value = pneu.tipo;
    document.getElementById('condicoes_climaticas').value = pneu.condicoes_climaticas;
    document.getElementById('eficiencia').value = pneu.eficiencia;
    document.getElementById('ruido').value = pneu.ruido;
    document.getElementById('marca').value = pneu.marca;
    document.getElementById('durabilidade').value = pneu.durabilidade;
    document.getElementById('quantidade').value = pneu.quantidade;
    
    pneuModal.show();
}

async function savePneu() {
    const id = document.getElementById('pneuId').value;
    const pneu = {
        dimensoes: document.getElementById('dimensoes').value,
        indice_carga: document.getElementById('indice_carga').value,
        indice_velocidade: document.getElementById('indice_velocidade').value,
        tipo: document.getElementById('tipo').value,
        condicoes_climaticas: document.getElementById('condicoes_climaticas').value,
        eficiencia: document.getElementById('eficiencia').value,
        ruido: document.getElementById('ruido').value,
        marca: document.getElementById('marca').value,
        durabilidade: document.getElementById('durabilidade').value,
        quantidade: document.getElementById('quantidade').value
    };
    
    try {
        if (id) {
            await fetch(`/api/pneus/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(pneu)
            });
        } else {
            await fetch('/api/pneus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(pneu)
            });
        }
        
        pneuModal.hide();
        loadPneus();
    } catch (error) {
        console.error('Erro ao salvar pneu:', error);
    }
}

async function deletePneu(id) {
    if (!confirm('Tem certeza que deseja excluir este pneu?')) return;
    
    try {
        await fetch(`/api/pneus/${id}`, {
            method: 'DELETE'
        });
        loadPneus();
    } catch (error) {
        console.error('Erro ao excluir pneu:', error);
    }
} 