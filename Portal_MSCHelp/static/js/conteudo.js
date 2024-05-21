
    function carregarTemplate(rota) {
        fetch(rota)
            .then(response => response.text())
            .then(html => {
                document.getElementById('conteudo').innerHTML = html;
            })
            .catch(error => console.error('Erro ao carregar o template:', error));
    }
