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
    const geometry = new THREE.BoxGeometry(4, 4, 4); // Ajuste o tamanho do cubo aqui (aumentado para 3x3x3)
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
        const planeGeometry = new THREE.PlaneGeometry(5, 4); // Ajuste o tamanho da imagem aqui (aumentado para 2.5x2.5)
        const planeMaterial = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        scene.add(plane);
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
});
