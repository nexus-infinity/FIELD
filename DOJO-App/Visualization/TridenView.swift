import SwiftUI
import SceneKit

struct TridenView: View {
    @State private var rotation: Double = 0
    @State private var fieldStrength: Double = 1.0
    @State private var isMonitoring: Bool = false
    
    // MARK: - Node Properties
    private let ob1Node = "●"  // OBI-WAN node
    private let tataNode = "▼" // TATA node
    private let atlasNode = "▲" // ATLAS node
    private let dojoNode = "■" // DOJO node
    
    var body: some View {
        VStack {
            // 3D Visualization
            SceneView(
                scene: createTridenScene(),
                options: [.allowsCameraControl, .autoenablesDefaultLighting]
            )
            .gesture(DragGesture()
                .onChanged { value in
                    rotation += value.translation.width
                }
            )
            
            // Controls
            VStack(spacing: 20) {
                // Field Strength Control
                VStack(alignment: .leading) {
                    Text("Field Strength: \(fieldStrength, specifier: "%.2f")")
                    Slider(value: $fieldStrength, in: 0...2) {
                        Text("Field Strength")
                    }
                }
                
                // Monitoring Toggle
                Button(action: {
                    isMonitoring.toggle()
                }) {
                    Label(
                        isMonitoring ? "Stop Monitoring" : "Start Monitoring",
                        systemImage: isMonitoring ? "stop.fill" : "play.fill"
                    )
                }
                .buttonStyle(.bordered)
            }
            .padding()
        }
    }
    
    private func createTridenScene() -> SCNScene {
        let scene = SCNScene()
        
        // Create nodes with symbolic representation
        let ob1 = createNode(symbol: ob1Node, position: SCNVector3(x: 0, y: 2, z: 0), color: .blue)
        let tata = createNode(symbol: tataNode, position: SCNVector3(x: -2, y: -1, z: 0), color: .red)
        let atlas = createNode(symbol: atlasNode, position: SCNVector3(x: 2, y: -1, z: 0), color: .green)
        let dojo = createNode(symbol: dojoNode, position: SCNVector3(x: 0, y: -2, z: 0), color: .purple)
        
        // Add connections between nodes
        addConnection(from: ob1, to: tata, scene: scene)
        addConnection(from: tata, to: atlas, scene: scene)
        addConnection(from: atlas, to: dojo, scene: scene)
        addConnection(from: dojo, to: ob1, scene: scene)
        
        // Add nodes to scene
        scene.rootNode.addChildNode(ob1)
        scene.rootNode.addChildNode(tata)
        scene.rootNode.addChildNode(atlas)
        scene.rootNode.addChildNode(dojo)
        
        return scene
    }
    
    private func createNode(symbol: String, position: SCNVector3, color: UIColor) -> SCNNode {
        let node = SCNNode()
        
        // Create text geometry for symbol
        let text = SCNText(string: symbol, extrusionDepth: 0.1)
        text.font = UIFont.systemFont(ofSize: 1.0, weight: .bold)
        text.firstMaterial?.diffuse.contents = color
        
        // Create node geometry
        let sphere = SCNSphere(radius: 0.3)
        sphere.firstMaterial?.diffuse.contents = color.withAlphaComponent(0.3)
        
        // Combine text and sphere
        let textNode = SCNNode(geometry: text)
        textNode.position = SCNVector3(x: -0.2, y: -0.2, z: 0.3)
        node.addChildNode(textNode)
        
        let sphereNode = SCNNode(geometry: sphere)
        node.addChildNode(sphereNode)
        
        node.position = position
        return node
    }
    
    private func addConnection(from: SCNNode, to: SCNNode, scene: SCNScene) {
        let line = SCNGeometry.line(from: from.position, to: to.position)
        let lineNode = SCNNode(geometry: line)
        lineNode.geometry?.firstMaterial?.diffuse.contents = UIColor.white.withAlphaComponent(0.5)
        scene.rootNode.addChildNode(lineNode)
    }
}

// MARK: - Helper Extensions
extension SCNGeometry {
    static func line(from: SCNVector3, to: SCNVector3) -> SCNGeometry {
        let indices: [Int32] = [0, 1]
        let source = SCNGeometrySource(vertices: [from, to])
        let element = SCNGeometryElement(indices: indices, primitiveType: .line)
        return SCNGeometry(sources: [source], elements: [element])
    }
}

// MARK: - Preview Provider
struct TridenView_Previews: PreviewProvider {
    static var previews: some View {
        TridenView()
    }
}
