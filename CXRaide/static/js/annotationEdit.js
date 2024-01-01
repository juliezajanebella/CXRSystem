document.addEventListener('DOMContentLoaded', function () {
    // element references
    var boxButton = document.getElementById('box-button');
    var pointButton = document.getElementById('point-button');
    var abnormalitiesDropdown = document.getElementById('abnormalities');


    // konva stage and layer setup
    var stage = new Konva.Stage({
        container: 'box-container',
        width: 415.99,
        height: 380,
    });
    var layer = new Konva.Layer();
    stage.add(layer);


    // stage variables
    var addingPoints = false;
    var currentGroup;
    var currentTransformer;
    var pointTransformer;


    // utility functions
    function updateTextBackground(label, background) {
        // Adjust the size and position to match the label
        background.width(label.width() + 20); // Padding of 10 on each side
        background.height(label.height() + 5); // Padding of 5 on top and bottom
        background.x(label.x() - 10);
        background.y(label.y() - 4);
        background.visible(true); // Ensure background is visible
        layer.batchDraw();
    }
    function createPointTransformer() {
        pointTransformer = new Konva.Transformer({
            enabledAnchors: ['top-left', 'top-right', 'bottom-left', 'bottom-right'],
            rotateEnabled: false, 
            anchorSize: 4, 
            borderDash: [3, 3],
            keepRatio: true, 
            centeredScaling: true, 
            visible: false
        });
        layer.add(pointTransformer);
    }
    function attachTransformerToPoint(point) {  // create and handle the transformer for points
        // ensure the existing transformer is detached
        if (currentTransformer) {
            currentTransformer.detach();
            layer.draw();
        }
        // check if pointTransformer is already created or not
        if (!pointTransformer) {
            pointTransformer = new Konva.Transformer({
                rotateEnabled: false,
                keepRatio: false,
                centeredScaling: true,
                borderDash: [3, 3],
                anchorSize: 8,
                anchorStroke: 'blue',
                anchorFill: 'lightblue',
                visible: false // Initially invisible
        });
        layer.add(pointTransformer);
        }
        // attach the transformer to the point
        pointTransformer.nodes([point]);
        pointTransformer.visible(true);
        pointTransformer.moveToTop(); // Ensure the transformer is on top of other elements
        layer.draw();
    }
    function handlePointClick(point) {
        pointTransformer.nodes([point]);
        pointTransformer.visible(true);
        layer.draw();
    }


    // main functionality
    function createBox() {
        var group = new Konva.Group({ draggable: true });
        var box = new Konva.Rect({
            x: 0, 
            y: 0, 
            width: 100, 
            height: 100,
            fill: 'rgba(0,0,0,0.5)', 
            stroke: 'black', 
            strokeWidth: 1,
            name:'box'
        });
        group.add(box);
        layer.add(group);
        
        var textBackground = new Konva.Rect({ // create a transparent background for the label
            x: 0,
            y: -20,
            fill: 'white',
            opacity: 0.5,
            visible: false, // make it visible by default
            listening: false // ignore mouse events
        });
        var label = new Konva.Text({ // create a label above the box
            x: 0,
            y: -20,
            text: "",
            fontSize: 14,
            fontFamily: 'Calibri',
            fill: 'black',
            listening: false // ignore mouse events
        });

        // update the background size based on the label size
        textBackground.width(label.width() + 20); // Padding of 10 on each side
        textBackground.height(label.height() + 5); // Padding of 5 on top and bottom
        group.add(box);

        // initial update for the text background size
        updateTextBackground(label, textBackground);
        label.text(abnormalitiesDropdown.options[abnormalitiesDropdown.selectedIndex].text);
        updateTextBackground(label, textBackground);

        var transformer = new Konva.Transformer({
            nodes: [box],
            rotateEnabled: false, // disable rotation
            flipEnabled: false, // diable flipping
            anchorSize: 8,
            borderDash: [3, 3], 
            keepRatio: false, 
            centeredScaling: true
        });

        layer.add(transformer);
        group.add(textBackground);
        group.add(label);

        box.points = []

        box.on('click', function () {
            currentGroup = group;
            currentTransformer = transformer;
            transformer.nodes([box]);
            layer.draw();
        });
        transformer.on('transform', function () { // add transformer listeners to update label position on box resize
            // adjust label position and text background size
            label.x(box.x() - 10);
            label.y(box.y() - 20);
            textBackground.x(label.x() - 10);
            textBackground.y(label.y() - 5);
            textBackground.width(label.width() + 20);
            textBackground.height(label.height() + 5);
            layer.batchDraw();
        });
        group.on('dragend transformend', function() {
            updateTextBackground(label, textBackground);
        });

        return { group, box, transformer, label, textBackground};
    }
    
    // event listeners
    boxButton.addEventListener('click', function() {
        var elements = createBox();
        currentGroup = elements.group;
        currentTransformer = elements.transformer;
        abnormalitiesDropdown.selectedIndex = 0; // Reset the dropdown
        
        // Reset the label text of the newly created box (if needed)
        elements.label.text("Abnormality:"); // Replace "Default Text" with whatever default you want
        updateTextBackground(elements.label, elements.textBackground); // Update the background size for new label text
        layer.draw();
    });
    pointButton.addEventListener('click', function() {
        addingPoints = !addingPoints;
        stage.container().style.cursor = addingPoints ? 'crosshair' : 'default'; // Change cursor on POINT button click
    });
    abnormalitiesDropdown.addEventListener('change', function() {
        if (currentGroup) {
            var label = currentGroup.children.find(child => child.className === 'Text');
            if (label) {
                label.text(this.options[this.selectedIndex].text);
                layer.draw();
            }
        }
    });


    // logic handle stage on click
    stage.on('click', function (e) {
        if (addingPoints && currentGroup && e.target === currentGroup.children[0]) {
            var box = currentGroup.children[0];
            var relativePos = currentGroup.getRelativePointerPosition();
            var point = new Konva.Circle({
                x: relativePos.x, 
                y: relativePos.y, 
                radius: 3, 
                fill: 'red',
                draggable: true,
                dragBoundFunc: function(pos) {
                    // Get the absolute position of the box
                    var boxAbsPos = box.getAbsolutePosition();
                    // Get the size of the box
                    var boxWidth = box.width() * box.scaleX();
                    var boxHeight = box.height() * box.scaleY();
                    // Calculate the bounds
                    var newX = Math.max(boxAbsPos.x, Math.min(pos.x, boxAbsPos.x + boxWidth));
                    var newY = Math.max(boxAbsPos.y, Math.min(pos.y, boxAbsPos.y + boxHeight));
                    // Return the new constrained position
                    return {
                        x: newX,
                        y: newY
                    };
                }
            });

            // Add the new point to the current box's list of points
            if (currentGroup.children[0].points) {
                currentGroup.children[0].points.push(point);
            }

            point.on('click', () => handlePointClick(point));
            currentGroup.add(point);
            layer.draw();
        } else if (e.target.getClassName() === 'Circle') {
            handlePointClick(e.target);
        } else if (e.target === stage) {
            if (currentTransformer) {
                currentTransformer.nodes([]);
                layer.draw();
            }
            if (pointTransformer) {
                pointTransformer.visible(false);
                layer.draw();
            }
        } 
        
        if (e.target.getClassName() === 'Circle') {
            // Stop event propagation to prevent selecting the box
            e.cancelBubble = true;
            
            // Attach the transformer to the clicked point
            attachTransformerToPoint(e.target);
        }
    });
    window.addEventListener('keydown', function(e) {
        if (e.key === 'Delete') {
            // Check if the point transformer has a selected node
            if (pointTransformer && pointTransformer.nodes().length > 0) {
                // Delete the selected point
                pointTransformer.nodes().forEach(function(node) {
                    node.destroy();
                });
                pointTransformer.nodes([]);
                pointTransformer.visible(false);
                layer.draw();
            } else if (currentTransformer && currentTransformer.nodes().length > 0) {
                // Delete the selected box and its associated points
                var nodes = currentTransformer.nodes();
                nodes.forEach(function(node) {
                    if (node.points) {
                        node.points.forEach(function(point) {
                            point.destroy();
                        });
                    }
                    node.getParent().destroy(); // node.parent.destroy() will destroy the group, which includes the box, label, and background
                    node.destroy();
                });
                currentTransformer.detach();
                currentTransformer.destroy();
                currentTransformer = null;
                currentGroup = null;
                layer.draw();
            }
        }
    });
    createPointTransformer();
});

// HERE FOR ZOOM

document.addEventListener('DOMContentLoaded', function () {
    var zoomInButton = document.getElementById('zoom-in-button'); // Assuming you have this button in your HTML
    var zoomOutButton = document.getElementById('zoom-out-button'); // Assuming you have this button in your HTML
    var imageToZoom = document.getElementById('image-to-zoom');
    var divContainer = document.getElementById('raw_cxray_image_div');
    var zoomScale = 1;
    var maxZoomScale = 5;
    var minZoomScale = 1; // Minimum zoom scale, usually 1 for original size
    var isDragging = false;
    var lastPosX = 0;
    var lastPosY = 0;

    function applyZoom(newScale) {
        zoomScale = newScale;

        imageToZoom.style.transform = `scale(${zoomScale})`;
        imageToZoom.style.transformOrigin = 'top left';

        // Toggle overflow based on zoom scale
        divContainer.style.overflow = zoomScale > 1 ? 'auto' : 'hidden';
    }

    function zoomIn() {
        var newScale = Math.min(zoomScale * 1.2, maxZoomScale); // Increase zoom
        applyZoom(newScale);
    }

    function zoomOut() {
        var newScale = Math.max(zoomScale / 1.2, minZoomScale); // Decrease zoom
        applyZoom(newScale);
    }

    zoomInButton.addEventListener('click', zoomIn);
    zoomOutButton.addEventListener('click', zoomOut);

    imageToZoom.addEventListener('mousedown', function (e) {
        isDragging = true;
        lastPosX = e.clientX;
        lastPosY = e.clientY;
    });
    
    document.addEventListener('mouseup', function () {
        isDragging = false;
    });
    
    document.addEventListener('mousemove', function (e) {
        if (isDragging) {
            var deltaX = e.clientX - lastPosX;
            var deltaY = e.clientY - lastPosY;
            lastPosX = e.clientX;
            lastPosY = e.clientY;
    
            var imgRect = imageToZoom.getBoundingClientRect();
    
            imageToZoom.style.left = (imgRect.left + deltaX) + 'px';
            imageToZoom.style.top = (imgRect.top + deltaY) + 'px';
        }
    });
});

// HERE FOR SAVING - not working check daw dri kiy hehe
// document.addEventListener('DOMContentLoaded', function () {
//     var saveButton = document.getElementById('save-button')

//     saveButton.addEventListener('click', function() {
//         var dataURL = stage.toDataURL({ pixelRatio: 3 });
//         downloadURL(dataURL, 'stage.png');
//     },false);

//     function downloadURL(url, name) {
//         var link = document.createElement('a');
//         link.download = name;
//         link.href = url;
//         document.body.appendChild(link);
//         link.click();
//         document.body.removeChild(link);
//         delete link;
//     }
// });

