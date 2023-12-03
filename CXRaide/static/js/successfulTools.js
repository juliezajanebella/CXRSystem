document.addEventListener('DOMContentLoaded', function () {
    var boxButton = document.getElementById('box-button');
    var pointButton = document.getElementById('point-button');
    var stage = new Konva.Stage({
        container: 'box-container',
        width: 500,
        height: 500,
    });

    var layer = new Konva.Layer();
    stage.add(layer);

    var addingPoints = false;
    var currentGroup;
    var currentTransformer;
    var pointTransformer;

    function createBox() {
        var group = new Konva.Group({ draggable: true });
        var box = new Konva.Rect({
            x: 0, y: 0, width: 100, height: 100,
            fill: 'rgba(0,0,0,0.5)', stroke: 'black', strokeWidth: 1
        });

        group.add(box);
        layer.add(group);

        var transformer = new Konva.Transformer({
            nodes: [box], rotateEnabled: false, anchorSize: 8,
            borderDash: [3, 3], keepRatio: false, centeredScaling: true
        });

        layer.add(transformer);

        box.points = []

        box.on('click', function () {
            currentGroup = group;
            currentTransformer = transformer;
            transformer.nodes([box]);
            layer.draw();
        });

        return { group, box, transformer };
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

    // Function to create and handle the transformer for points
    function attachTransformerToPoint(point) {
    // Ensure the existing transformer is detached
        if (currentTransformer) {
            currentTransformer.detach();
            layer.draw();
        }

        // Check if pointTransformer is already created or not
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
    
        // Attach the transformer to the point
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

    boxButton.addEventListener('click', function() {
        var elements = createBox();
        currentGroup = elements.group;
        currentTransformer = elements.transformer;
    });

    pointButton.addEventListener('click', function() {
        addingPoints = !addingPoints;
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
                    node.destroy();
                });
                currentTransformer.detach();
                currentTransformer.destroy();
                currentTransformer = null;
                layer.draw();
            }
        }
    });
    

    createPointTransformer();
});

// HERE FOR ZOOM

document.addEventListener('DOMContentLoaded', function () {
    var zoomButton = document.getElementById('zoom-button'); // The button to zoom in
    var imageToZoom = document.getElementById('image-to-zoom'); // The image to be zoomed
    var divContainer = document.getElementById('raw-cxray-div'); // The div container of the image
    var zoomScale = 1; // Current zoom level
    var maxZoomScale = 2; // Set a reasonable max zoom scale; you can adjust this as needed

    // Function to apply or reset zoom on the image
    function applyZoom(newScale) {
        // Update the zoom scale
        zoomScale = newScale;
    
        // Apply the transformation to the image
        imageToZoom.style.transform = `scale(${zoomScale})`;
        // Adjust the transform origin to ensure the image scales from the top-left corner
        imageToZoom.style.transformOrigin = 'top left';
    
        // Make sure the divContainer has overflow hidden to prevent the image from spilling out
        divContainer.style.overflow = 'auto';
    
        // Update the container's scrollable size based on the zoomScale
        divContainer.scrollWidth = imageToZoom.clientWidth * zoomScale;
        divContainer.scrollHeight = imageToZoom.clientHeight * zoomScale;
    }

    // Function to calculate and constrain the new zoom scale
    function calculateZoom(isZoomingIn) {
        var scaleFactor = isZoomingIn ? 1.2 : 1 / 1.2; // Factor by which the image is zoomed in or out
        var newScale = isZoomingIn ? zoomScale * scaleFactor : 1; // Calculate new scale or reset to original

        // Constrain zoom to not exceed the size of the div container
        var rect = divContainer.getBoundingClientRect();
        var imageRect = imageToZoom.getBoundingClientRect();
        if (imageRect.width * scaleFactor > rect.width || imageRect.height * scaleFactor > rect.height) {
            if (isZoomingIn) {
                newScale = Math.min(newScale, maxZoomScale); // Constrain to max zoom scale
            } else {
                newScale = 1; // Reset to original scale
            }
        }

        applyZoom(newScale);
    }

    // Event listener for the zoom button to zoom in
    zoomButton.addEventListener('click', function() {
        calculateZoom(true); // Zoom in
    });

    // Event listener for the image to zoom out on click
    imageToZoom.addEventListener('click', function () {
        calculateZoom(false); // Zoom out (reset)
    });

    // ... Your existing Konva.js setup and functionality ...

});
