import SwiftUI
import SceneKit

struct TetrahedralView: View {
    @State private var cameraPosition: SCNVector3 = SCNVector3(0, 0, 5)
    @State private var isDebugMode: Bool = false
    
    // MARK: - Node Properties
    private let ob1Node = "●"  // OBI-WAN node
    private let tataNode = "▼" // TATA node
    private let atlasNode = "▲" // ATLAS node
    private let dojoNode = "■" // DOJO node
    
    var body: some View {
        ZStack {
            SceneView(
                scene: createTetrahedralScene(),
                pointOfView: createCamera(),
                options: [.allowsCameraControl, .autoenablesDefaultLighting, .temporalAntialiasingEnabled]
            )
            
            // Debug overlay
            if isDebugMode {
                VStack {
                    Text("Camera Position: \(String(format: "%.2f, %.2f, %.2f", cameraPosition.x, cameraPosition.y, cameraPosition.z))")
                        .padding()
                        .background(Color.black.opacity(0.7))
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
                .padding()
            }
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: { isDebugMode.toggle() }) {
                    Image(systemName: isDebugMode ? "eye.fill" : "eye")
                }
            }
        }
    }
    
    private func createTetrahedralScene() -> SCNScene {
        let scene = SCNScene()
        
        // Create nodes with symbolic representation
        let ob1 = createNode(symbol: ob1Node, position: SCNVector3(x: 0, y: 1, z: 0), color: .blue)
        let tata = createNode(symbol: tataNode, position: SCNVector3(x: -1, y: -1, z: 0), color: .red)
        let atlas = createNode(symbol: atlasNode, position: SCNVector3(x: 1, y: -1, z: 0), color: .green)
        let dojo = createNode(symbol: dojoNode, position: SCNVector3(x: 0, y: 0, z: -1), color: .purple)
        
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
    
    private func createCamera() -> SCNNode {
        let camera = SCNCamera()
        let cameraNode = SCNNode()
        cameraNode.camera = camera
        cameraNode.position = cameraPosition
        return cameraNode
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
struct TetrahedralView_Previews: PreviewProvider {
    static var previews: some View {
        TetrahedralView()
    }
}
