document.addEventListener('DOMContentLoaded', function () {
    var boxButton = document.getElementById('box-button');
    var stage = new Konva.Stage({
        container: 'box-container',
        width: 500,
        height: 500,
    });

    var layer = new Konva.Layer();
    stage.add(layer);

    var currentTransformer;

    // Function to create a new box and transformer
    function createBox() {
        var box = new Konva.Rect({
            x: 90,
            y: 90,
            width: 100,
            height: 100,
            fill: 'rgba(0,0,0,0.5)',
            stroke: 'black',
            strokeWidth: 1,
            draggable: true
        });

        var transformer = new Konva.Transformer({
            rotateEnabled: false,
            anchorStroke: 'blue',
            anchorFill: 'lightblue',
            anchorSize: 8,
            borderStroke: 'blue',
            borderDash: [3, 3],
            keepRatio: false,
            centeredScaling: true
        });

        box.on('click', function () {
            currentTransformer = transformer;
            transformer.nodes([box]);
            layer.draw();
        });

        layer.add(box);
        layer.add(transformer);
        transformer.nodes([box]);
        currentTransformer = transformer;
        layer.draw();
    }

    // Click event to remove the transformer when clicking outside of any box
    stage.on('click', function (e) {
        if (e.target === stage) {
            if (currentTransformer) {
                currentTransformer.nodes([]);
                layer.draw();
            }
        }
    });

    // Event listener for the 'BOX' button to create a new box
    boxButton.addEventListener('click', function() {
        createBox();
    });

    // Event listener for keydown to handle deletion of the box
    window.addEventListener('keydown', function (e) {
        if (e.key === 'Delete' && currentTransformer && currentTransformer.nodes().length > 0) {
            // Remove the current box and transformer from the layer
            currentTransformer.nodes().forEach(function (node) {
                node.destroy();
            });
            currentTransformer.destroy();
            currentTransformer = null;
            layer.draw();
        }
    });
});
