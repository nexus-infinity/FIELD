import SwiftUI
import SceneKit

struct FieldVisualizerView: View {
    @State private var fieldData: [Double] = Array(repeating: 0.5, count: 4) // Initial values for 4 nodes
    @State private var selectedNode: Int? = nil
    @State private var isMonitoring: Bool = false
    @State private var resonanceThreshold: Double = 0.85 // From Arcadian architecture
    
    // MARK: - Node Properties
    private let nodeSymbols = ["●", "▼", "▲", "■"]
    private let nodeNames = ["OBI-WAN", "TATA", "ATLAS", "DOJO"]
    private let nodeColors: [Color] = [.blue, .red, .green, .purple]
    
    var body: some View {
        VStack {
            // Field visualization area
            ZStack {
                // Connection lines
                ForEach(0..<4) { i in
                    ForEach((i+1)..<4) { j in
                        ConnectionLine(
                            start: nodePosition(for: i),
                            end: nodePosition(for: j),
                            strength: min(fieldData[i], fieldData[j])
                        )
                    }
                }
                
                // Nodes
                ForEach(Array(fieldData.enumerated()), id: \.offset) { index, strength in
                    FieldNodeView(
                        symbol: nodeSymbols[index],
                        name: nodeNames[index],
                        strength: strength,
                        color: nodeColors[index],
                        isSelected: selectedNode == index,
                        position: nodePosition(for: index)
                    )
                    .onTapGesture {
                        selectedNode = index
                    }
                }
            }
            .frame(height: 300)
            .padding()
            
            // Controls and info
            VStack(spacing: 20) {
                // Selected node controls
                if let selected = selectedNode {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("\(nodeNames[selected]) Node")
                            .font(.headline)
                        
                        Text("Field Strength: \(fieldData[selected], specifier: "%.2f")")
                        
                        Slider(value: $fieldData[selected], in: 0...2) {
                            Text("Adjust Field Strength")
                        }
                        
                        if fieldData[selected] >= resonanceThreshold {
                            Text("Resonance Achieved")
                                .foregroundColor(.green)
                        } else {
                            Text("Below Resonance Threshold")
                                .foregroundColor(.orange)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                }
                
                // Monitoring controls
                HStack {
                    Button(action: {
                        isMonitoring.toggle()
                        if isMonitoring {
                            startFieldMonitoring()
                        }
                    }) {
                        Label(
                            isMonitoring ? "Stop Monitoring" : "Start Monitoring",
                            systemImage: isMonitoring ? "stop.fill" : "play.fill"
                        )
                    }
                    .buttonStyle(.bordered)
                    
                    if isMonitoring {
                        Text("Monitoring Active")
                            .foregroundColor(.green)
                    }
                }
            }
            .padding()
        }
    }
    
    private func nodePosition(for index: Int) -> CGPoint {
        let radius: CGFloat = 120
        let angle = 2 * .pi * CGFloat(index) / 4
        return CGPoint(
            x: radius * cos(angle),
            y: radius * sin(angle)
        )
    }
    
    private func startFieldMonitoring() {
        // Simulated field monitoring
        // In production, this would connect to the real field monitoring system
        Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { timer in
            guard isMonitoring else {
                timer.invalidate()
                return
            }
            
            // Simulate field strength changes
            withAnimation {
                for i in 0..<fieldData.count {
                    fieldData[i] += Double.random(in: -0.1...0.1)
                    fieldData[i] = max(0, min(2, fieldData[i]))
                }
            }
        }
    }
}

// MARK: - Supporting Views
struct FieldNodeView: View {
    let symbol: String
    let name: String
    let strength: Double
    let color: Color
    let isSelected: Bool
    let position: CGPoint
    
    var body: some View {
        VStack {
            ZStack {
                Circle()
                    .fill(color.opacity(0.3))
                    .frame(width: 60, height: 60)
                
                Text(symbol)
                    .font(.title)
                    .foregroundColor(color)
            }
            .overlay(
                Circle()
                    .stroke(isSelected ? Color.yellow : Color.clear, lineWidth: 2)
                    .frame(width: 62, height: 62)
            )
            
            if isSelected {
                Text(name)
                    .font(.caption)
                    .foregroundColor(color)
            }
        }
        .position(x: position.x + 150, y: position.y + 150)
    }
}

struct ConnectionLine: View {
    let start: CGPoint
    let end: CGPoint
    let strength: Double
    
    var body: some View {
        Path { path in
            path.move(to: CGPoint(x: start.x + 150, y: start.y + 150))
            path.addLine(to: CGPoint(x: end.x + 150, y: end.y + 150))
        }
        .stroke(Color.white.opacity(strength / 2), lineWidth: 2)
    }
}

// MARK: - Preview Provider
struct FieldVisualizerView_Previews: PreviewProvider {
    static var previews: some View {
        FieldVisualizerView()
    }
}
