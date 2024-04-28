

import * as THREE from 'three';
import Stats from 'three/addons/libs/stats.module.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
// import { LinearToSRGB } from 'three/src/math/ColorManagement';


const sliders = [
    "#slider1", "#slider2", "#slider3", "#slider4", "#slider5", "#slider6",
    "#sliderw1", "#sliderw2", "#sliderX", "#sliderY", "#sliderZ", "#sliderR", "#sliderP", "#sliderYaw"
  ];
  
  const increaseButtons = [
    "#increaseArm1", "#increaseArm2", "#increaseArm3", "#increaseArm4", "#increaseArm5", "#increaseArm6",
    "#increaseW1", "#increaseW2", "#increaseArmX", "#increaseArmY", "#increaseArmZ", "#increaseArmR", "#increaseArmP", "#increaseArmYaw"
  ];
  
  const decreaseButtons = [
    "#decreaseArm1", "#decreaseArm2", "#decreaseArm3", "#decreaseArm4", "#decreaseArm5", "#decreaseArm6",
    "#decreaseW1", "#decreaseW2", "#decreaseArmX", "#decreaseArmY", "#decreaseArmZ", "#decreaseArmR", "#decreaseArmP", "#decreaseArmYaw"
  ];
  
  const valueElements = [
    "#arm-n-1", "#arm-n-2", "#arm-n-3", "#arm-n-4", "#arm-n-5", "#arm-n-6",
    "#wheel-n-1", "#wheel-n-2", "#arm-n-X", "#arm-n-Y", "#arm-n-Z", "#arm-n-R", "#arm-n-P", "#arm-n-Yaw"
  ];
  
  const lockElements = [
    "#switch1", "#switch2", "#switch3", "#switch4", "#switch5", "#switch6",
    "#switchw1", "#switchw2", "#switchX", "#switchY", "#switchZ", "#switchR", "#switchP", "#switchYaw"
  ];
  
  const directionButtons = [
    "#forward", "#reverse", "#right", "#left"
  ];
  
  const getInverseLabels = [
    "#armI-n-X", "#armI-n-Y", "#armI-n-Z", "#armI-n-R", "#armI-n-P", "#armI-n-Yaw"
  ];
  
  const getDirectLabels = [
    "#armd-n-1", "#armd-n-2", "#armd-n-3", "#armd-n-4", "#armd-n-5", "#armd-n-6"
  ];
  
  
  
  function pause(ms) {
    return new Promise(resolve => setTimeout(resolve, ms * 1000));
  }
  
  function updateSliderValue(index) {
      document.querySelector(valueElements[index]).textContent = document.querySelector(sliders[index]).value;
      switch (sliders[index]) {
          case sliders[0]:
              setClaw_2Rotation(document.querySelector(sliders[index]).value);
              break;
          case sliders[1]:
              setClaw_1Rotation(document.querySelector(sliders[index]).value);
              break;
          case sliders[2]:
              setWristRotation(document.querySelector(sliders[index]).value);
              break;
          case sliders[3]:
              setForeArmRotation(document.querySelector(sliders[index]).value);
              break;
          case sliders[4]:
              setArmRotation(document.querySelector(sliders[index]).value);
              break;
          case sliders[5]:
              setShoulderRotation(document.querySelector(sliders[index]).value); 
              break;      
          default:
      }  
  }
  
  function increase(index) {
      document.querySelector(sliders[index]).value = parseInt(document.querySelector(sliders[index]).value) + 1;
    updateSliderValue(index);
  }
  
  function decrease(index) {
      document.querySelector(sliders[index]).value -= 1;
    updateSliderValue(index);
  }
  
  
  
  sliders.forEach((slider, index) => {
    const element = document.querySelector(slider);
    const valueElement = document.querySelector(valueElements[index]);
  
    element.addEventListener("input", async (event) => {
      valueElement.textContent = event.currentTarget.value
      switch (sliders[index]) {
          case sliders[0]:
              setClaw_2Rotation(event.currentTarget.value);
              break;
          case sliders[1]:
              setClaw_1Rotation(event.currentTarget.value);
              break;
          case sliders[2]:
              setWristRotation(event.currentTarget.value);
              break;
          case sliders[3]:
              setForeArmRotation(event.currentTarget.value);
              break;
          case sliders[4]:
              setArmRotation(event.currentTarget.value);
              break;
          case sliders[5]:
              setShoulderRotation(event.currentTarget.value); 
              break;      
          default:
          
        }
      
      // Aquí puedes continuar con el resto de tu lógica específica para el slider
    });
  });
  
  increaseButtons.forEach((button, index) => {
    const element = document.querySelector(button);
    element.addEventListener("click", () => increase(index));
  });
  
  decreaseButtons.forEach((button, index) => {
    const element = document.querySelector(button);
    element.addEventListener("click", () => decrease(index));
  });



const sendButton = document.querySelector("#sendButton")
const stabswitch = document.querySelector("#switchStab")


stabswitch.addEventListener("change", (event) => {
    if (stabswitch.checked) {
        enviarMensajeMQTT('/turtlebot/stab/set',1);
        console.log(1)
    }
    else {
        enviarMensajeMQTT('/turtlebot/stab/set',0);
        console.log(0)
    }
});


sendButton.addEventListener("click", enviarPos);

var label1 = document.querySelector(getInverseLabels[0])
var label2 = document.querySelector(getInverseLabels[1])
var label3 = document.querySelector(getInverseLabels[2])
var label4 = document.querySelector(getInverseLabels[3])
var label5 = document.querySelector(getInverseLabels[4])
var label6 = document.querySelector(getInverseLabels[5])


function refreshLabels(stats) {
    label1.textContent = stats.posX 
    label2.textContent = stats.posY 
    label3.textContent = stats.posZ 
    label4.textContent = stats.posR 
    label5.textContent = stats.posP 
    label6.textContent = stats.posYaw 
}

function enviarPos() {
    const dxl7 = document.querySelector(valueElements[0]).textContent;
    const dxl6 = document.querySelector(valueElements[1]).textContent;
    const dxl5 = document.querySelector(valueElements[2]).textContent;
    const dxl4 = document.querySelector(valueElements[3]).textContent;
    const dxl3 = document.querySelector(valueElements[4]).textContent;
    const dxl2 = document.querySelector(valueElements[5]).textContent;
       
    const positionQ = dxl2+" "+dxl3+" "+dxl4+" "+dxl5+" "+dxl6+" "+dxl7;

    console.log(positionQ);

    enviarMensajeMQTT('/turtlebot/arm/set/', positionQ);

}


function enviarMensajeMQTT(topic, msg) {
    var data = {
        'topic': topic,
        'msg': msg
    };

    // Envía el mensaje al servidor Flask en tiempo real usando una solicitud HTTP POST
    fetch('/publish', {
        method: 'POST',
        body: JSON.stringify(data), // Envía el valor como JSON
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            // Maneja la respuesta del servidor si es necesario
            console.log(data);
            refreshLabels(data)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function getinverse() {
    fetch('/get_label_value')
    .then(response => response.json())
    .then(data => {
        document.getElementById('armI-n-X').textContent = data.posX;
        document.getElementById('armI-n-Y').textContent = data.posY;
        document.getElementById('armI-n-Z').textContent = data.posZ;
        document.getElementById('armI-n-R').textContent = data.posR;
        document.getElementById('armI-n-P').textContent = data.posP;
        document.getElementById('armI-n-Yaw').textContent = data.posYaw;
    })
}

function getDirect() {
    fetch('/get_label_value')
    .then(response => response.json())
    .then(data => {
        document.getElementById('armd-n-1').textContent = data.q1;
        document.getElementById('armd-n-2').textContent = data.q2;
        document.getElementById('armd-n-3').textContent = data.q3;
        document.getElementById('armd-n-4').textContent = data.q4;
        document.getElementById('armd-n-5').textContent = data.q5;
        document.getElementById('armd-n-6').textContent = data.q6;
    })
}




let camera, scene, renderer, stats;

const clock = new THREE.Clock();

let Robot, Wheel_L, Wheel_R, Shoulder, Arm, ForeArm, Wrist, Claw_1, Claw_2;

let modelsLoaded = 0, hadLoaded = false;

init();
animate();

//Delet me plz!!
//#region extra tools
//#endregion

//------------------------------- funciones para nico -------------------------------------------------

/**
 * Update robots position and rotation values
 * @param  {number} x X position of the robot
 * @param  {number} y Y position of the robot
 * @param  {number} r Y axix rotation value of the robot
 */
function setRobotPosition(x, y, r) {
    Robot.position.set(x, y, Robot.position.z);
    Robot.rotation.y = r;
}

/**
 * Update wheels rotation value
 * @param  {number} r Z axis rotation value of Wheel_R
 * @param  {number} l Z axis rotation value of Wheel_L
 */
function setWheelRotation(r, l) {
    Robot.position.set(x, y, Robot.position.z);
    Robot.rotation.y = r;
}

/**
 * Update Shoulder rotation value
 * @param  {number} r Y axis rotation value of the Shoulder (0 - 100)
 */
function setShoulderRotation(r) {
    var value = map(r, -150, 150, -0.83*Math.PI, 0.83*Math.PI)
    console.log("Shoulder Y:", value);
    Shoulder.rotation.y = value;
}

/**
 * Update Arm rotation value
 * @param  {number} r X axis rotation value of the arm (0 - 100)
 */
function setArmRotation(r) {
    var value = map(r, -128, 124, -2.4, 2.4)
    console.log("arm X:", value);
    Arm.rotation.x = value;
}

/**
 * Update ForeArm rotation value
 * @param  {number} r X axis rotation value of the ForeArm (0 - 100)
 */
function setForeArmRotation(r) {
    var value = map(r, -149, 149, -2.4, 2.4)
    console.log("ForeArm X:", value);
    ForeArm.rotation.x = value;
}

/**
 * Update Wrist rotation value
 * @param  {number} r X axis rotation value of the Wrist (0 - 100)
 */
function setWristRotation(r) {
    var value = map(r, -101, 103, -2, 2)
    console.log("Wrist X:", value);
    Wrist.rotation.x = value;
}

/**
 * Update Claw_1 rotation value
 * @param  {number} r Y axis rotation value of the Claw_1 (0 - 100)
 */
function setClaw_1Rotation(r) {
    var value = map(r, -150, 150, -0.833*Math.PI, 0.833*Math.PI)
    console.log("Claw_1 Y:", value);
    Claw_1.rotation.y = value;
}

/**
 * Update Claw_2 rotation value
 * @param  {number} r X axis rotation value of the Claw_2 (0 - 100)
 */
function setClaw_2Rotation(r) {
    var value = map(r, 62.5, 0, 0, 2.8)
    console.log("Claw_2 X:", value);
    Claw_2.rotation.x = value;
}


//------------------------------- THREE js -------------------------------------------------

function init() {

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000);
    camera.position.set(100, 400, 1000);

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x00ADB5);
    // scene.fog = new THREE.Fog(0xa0a0a0, 800, 3000);

    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 5);
    hemiLight.position.set(0, 200, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 5);
    dirLight.position.set(0, 200, 100);
    dirLight.castShadow = true;
    dirLight.shadow.camera.top = 180;
    dirLight.shadow.camera.bottom = - 100;
    dirLight.shadow.camera.left = - 120;
    dirLight.shadow.camera.right = 120;
    scene.add(dirLight);

    // scene.add( new THREE.CameraHelper( dirLight.shadow.camera ) );

    // ground
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(4000, 4000), new THREE.MeshPhongMaterial({ color: 0x393E46, depthWrite: false }));
    mesh.rotation.x = - Math.PI / 2;
    mesh.receiveShadow = true;
    scene.add(mesh);

    const grid = new THREE.GridHelper(4000, 60, 0x000000, 0x000000);
    grid.material.opacity = 0.2;
    grid.material.transparent = true;
    scene.add(grid);

    // model
    const loader = new FBXLoader();
    loader.load('/get_fbx/Robot.fbx', addFBX);
    loader.load('/get_fbx/Wheel_L.fbx', addFBX);
    loader.load('/get_fbx/Wheel_R.fbx', addFBX);
    loader.load('/get_fbx/Shoulder.fbx', addFBX);
    loader.load('/get_fbx/ForeArm.fbx', addFBX);
    loader.load('/get_fbx/Arm.fbx', addFBX);
    loader.load('/get_fbx/Wrist.fbx', addFBX);
    loader.load('/get_fbx/Claw_1.fbx', addFBX);
    loader.load('/get_fbx/Claw_2.fbx', addFBX);

    const canvaSim = document.querySelector(".sim")

    renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvaSim });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(canvaSim.clientWidth, canvaSim.clientHeight);
    renderer.shadowMap.enabled = true;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 300, 0);
    controls.update();

    window.addEventListener('resize', canvaSim.onWindowResize);

    // stats
    stats = new Stats();
    canvaSim.appendChild(stats.dom);

}

function addFBX(object) {

    object.traverse(function (child) {

        if (child.isMesh) {

            child.castShadow = true;
            child.receiveShadow = true;

            switch (child.name) {
                case "Robot": Robot = object;
                    break;

                case "Wheel_L": Wheel_L = object;
                    break;

                case "Wheel_R": Wheel_R = object;
                    break;

                case "Shoulder": Shoulder = object;
                    break;

                case "Arm": Arm = object;
                    break;

                case "ForeArm": ForeArm = object;
                    break;

                case "Wrist": Wrist = object;
                    break;

                case "Claw_1": Claw_1 = object;
                    break;

                case "Claw_2": Claw_2 = object;
                    break;

                default:
                    console.log(child.name);
            }
        }
    });

    modelsLoaded++;
    if (modelsLoaded === 9) {
        hadLoaded = true;
        ParentParts();
    }
}

function ParentParts() {
    //add objects to scene
    scene.add(Robot);
    scene.add(Wheel_L);
    scene.add(Wheel_R);
    scene.add(Shoulder);
    scene.add(Arm);
    scene.add(ForeArm);
    scene.add(Wrist);
    scene.add(Claw_1);
    scene.add(Claw_2);

    //parent objects
    Robot.add(Wheel_L);
    Robot.add(Wheel_R);

    Robot.add(Shoulder);
    Shoulder.add(Arm);
    Arm.add(ForeArm);
    ForeArm.add(Wrist);
    Wrist.add(Claw_1);
    Claw_1.add(Claw_2);

    //parts offset's
    Robot.position.set(0, 13, 0);
    Wheel_L.position.set(0, 23, -75);
    Wheel_R.position.set(0, 23, 75);

    Shoulder.position.set(43, 178, 0);
    Arm.position.set(0, 44, 0);
    ForeArm.position.set(0, 95, 0);
    Wrist.position.set(0, 94, 0);
    Claw_1.position.set(0, 75, 24);
    Claw_2.position.set(0, 23, 15);

    Shoulder.rotation.y = -Math.PI/2;
}

function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {

    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const time = clock.getElapsedTime()

    if (hadLoaded) {
        // Robot.rotation.y += 1 * delta;
        // Wheel_L.rotation.z += 1 * delta;
        // Wheel_R.rotation.z -= 1 * delta;

        // Shoulder.rotation.y += .2 * delta;
        // Arm.rotation.x = Math.sin(time);
        // ForeArm.rotation.x = Math.cos(time);
        // Wrist.rotation.x = Math.cos(time);

        // Claw_1.rotation.y += 1 * delta;
        // Claw_2.rotation.x = Math.sin(time);

        // console.log(Shoulder.rotation.y );

    }

    renderer.render(scene, camera);
    stats.update();
}

//----------------------- extra functions-------------------------
function map(current, in_min, in_max, out_min, out_max) {
    const mapped = ((current - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min;
    return clamp(mapped, out_min, out_max);
}

function clamp(input, min, max) {
    return input < min ? min : input > max ? max : input;
}
