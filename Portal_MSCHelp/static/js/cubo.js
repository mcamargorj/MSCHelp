document.addEventListener('DOMContentLoaded', function() {
    let rotation_direction = 1;  // Inicialmente, gira no sentido horário

    const canvas = document.getElementById('cubo');
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    canvas.appendChild(renderer.domElement);

    // Criar materiais transparentes para o cubo
    const geometry = new THREE.BoxGeometry(4, 4, 4); // Tamanho do cubo
    const material = new THREE.MeshBasicMaterial({ 
        color: 0x00ff00, 
        transparent: true, 
        opacity: 0.3, 
        wireframe: true 
    }); 
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    // Carregar a textura da imagem
    const textureLoader = new THREE.TextureLoader();
    textureLoader.load('/static/images/logo.png', function(texture) {
        const textureAspect = texture.image.width / texture.image.height;

        // Ajustar a geometria para manter a proporção da imagem
        const planeGeometry = new THREE.PlaneGeometry(6, 6 / textureAspect); // Ajustando a proporção
        const planeMaterial = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
        
        // Criar um plano e posicioná-lo no centro do cubo
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        
        // Posicionar o plano no centro do cubo (sem ser em uma face)
        plane.position.set(0, 0, 0);  // Posicionar no centro do cubo
        cube.add(plane);  // Adicionando o plano como filho do cubo (o plano vai girar junto com o cubo)
    });

    camera.position.z = 5.5; // Ajuste a posição da câmera para acomodar o cubo maior

    function animate() {
        requestAnimationFrame(animate);

        cube.rotation.x += 0.01 * rotation_direction;
        cube.rotation.y += 0.01 * rotation_direction;

        renderer.render(scene, camera);
    }

    animate();

    document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowLeft') {
            rotation_direction = -1;  // Girar para a esquerda
        } else if (event.key === 'ArrowRight') {
            rotation_direction = 1;   // Girar para a direita
        }
    });

    // Variáveis para detecção de toque
    let touchStartX = 0;

    // Evento para iniciar o toque
    canvas.addEventListener('touchstart', function(event) {
        touchStartX = event.touches[0].clientX; // Posição inicial do toque
    });

    // Evento para terminar o toque
    canvas.addEventListener('touchend', function(event) {
        const touchEndX = event.changedTouches[0].clientX; // Posição final do toque

        if (touchEndX < touchStartX) {
            rotation_direction = -1;  // Girar para a esquerda
        } else if (touchEndX > touchStartX) {
            rotation_direction = 1;   // Girar para a direita
        }
    });
});
