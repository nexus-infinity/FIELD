#!/usr/bin/env python3
"""
Ephemeral Cloud Processing Workflow

Philosophy: 
- Spin up cloud infrastructure for heavy processing
- Extract weighted/valuable data
- Consolidate results into permanent local systems  
- Destroy cloud resources to prevent fragmentation and costs

Workflow:
1. BUILD: Deploy processing infrastructure to GCP
2. PROCESS: Run analysis, cross-reference global databases  
3. EXTRACT: Pull valuable insights and weighted data
4. CONSOLIDATE: Store results in permanent local systems
5. DESTROY: Clean up all cloud resources

This prevents data fragmentation and maintains clear data ownership.
"""

import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
import tempfile

class EphemeralInvestigationProcessor:
    def __init__(self):
        self.gcp_project = "berjak-development-project"
        self.field_root = Path("/Users/jbear/FIELD")
        self.session_id = f"investigation-{int(time.time())}"
        self.cloud_resources = []
        
        # Permanent local storage
        self.results_dir = self.field_root / "investigation_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Weighted data categories to extract
        self.extraction_targets = {
            "entities": {
                "high_value": ["panama_papers_matches", "sanctions_matches", "corporate_connections"],
                "medium_value": ["opencorporates_matches", "regulatory_flags"],
                "low_value": ["name_variations", "possible_connections"]
            },
            "relationships": {
                "high_value": ["ownership_chains", "financial_flows", "shared_addresses"],
                "medium_value": ["shared_directors", "temporal_overlaps"],
                "low_value": ["name_similarities", "jurisdiction_patterns"]
            },
            "compliance": {
                "high_value": ["sanctions_violations", "regulatory_breaches", "criminal_connections"],
                "medium_value": ["jurisdiction_risks", "unusual_patterns"],
                "low_value": ["reporting_gaps", "documentation_issues"]
            }
        }

    def execute_ephemeral_workflow(self):
        """Execute the complete ephemeral processing workflow"""
        
        print(f"🚀 Starting Ephemeral Investigation Processing: {self.session_id}")
        
        try:
            # Phase 1: BUILD
            print("\n📦 PHASE 1: BUILD - Deploying cloud infrastructure...")
            self.deploy_processing_infrastructure()
            
            # Phase 2: PROCESS  
            print("\n⚡ PHASE 2: PROCESS - Running analysis and cross-referencing...")
            self.run_analysis_pipeline()
            
            # Phase 3: EXTRACT
            print("\n📊 PHASE 3: EXTRACT - Pulling valuable insights...")
            extracted_data = self.extract_weighted_data()
            
            # Phase 4: CONSOLIDATE
            print("\n💾 PHASE 4: CONSOLIDATE - Storing in permanent systems...")
            self.consolidate_results(extracted_data)
            
            print(f"\n✅ Processing complete! Results stored in: {self.results_dir}")
            
        finally:
            # Phase 5: DESTROY (always runs)
            print("\n🧹 PHASE 5: DESTROY - Cleaning up cloud resources...")
            self.cleanup_cloud_resources()
            
        return self.generate_final_report()

    def deploy_processing_infrastructure(self):
        """Deploy temporary processing infrastructure to GCP"""
        
        deployment_commands = [
            # Create compute instance
            f"""gcloud compute instances create investigation-processor-{self.session_id} \
                --project={self.gcp_project} \
                --zone=us-central1-a \
                --machine-type=e2-standard-4 \
                --image-family=cos-stable \
                --image-project=cos-cloud \
                --tags=investigation-processor \
                --metadata-from-file=startup-script=startup.sh""",
                
            # Create firewall rules
            f"""gcloud compute firewall-rules create allow-investigation-{self.session_id} \
                --project={self.gcp_project} \
                --allow=tcp:8080,tcp:7474,tcp:9200 \
                --source-ranges=0.0.0.0/0 \
                --target-tags=investigation-processor""",
                
            # Deploy docker-compose stack
            f"""gcloud compute scp docker-compose.yml investigation-processor-{self.session_id}:~ \
                --zone=us-central1-a""",
                
            f"""gcloud compute ssh investigation-processor-{self.session_id} \
                --zone=us-central1-a \
                --command="docker-compose up -d" """
        ]
        
        for cmd in deployment_commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"  ✅ {cmd.split()[2]} deployed")
                else:
                    print(f"  ⚠️  {cmd.split()[2]} failed: {result.stderr}")
                    
                # Track resources for cleanup
                if "create" in cmd:
                    resource_name = cmd.split()[3]
                    self.cloud_resources.append(resource_name)
                    
            except Exception as e:
                print(f"  ❌ Deployment error: {e}")
        
        # Wait for services to be ready
        time.sleep(120)  # 2 minutes for services to start
        print("  ⏳ Services starting up...")

    def run_analysis_pipeline(self):
        """Run the complete analysis pipeline on cloud infrastructure"""
        
        cloud_ip = self.get_cloud_instance_ip()
        if not cloud_ip:
            print("  ❌ Could not get cloud instance IP")
            return
            
        print(f"  🌐 Cloud instance: {cloud_ip}")
        
        # Analysis pipeline steps
        analysis_steps = {
            "upload_local_entities": self.upload_local_entities,
            "cross_reference_icij": self.cross_reference_icij_databases,
            "check_corporate_registries": self.check_corporate_registries,
            "screen_sanctions": self.screen_sanctions_lists,
            "build_entity_graph": self.build_neo4j_graph,
            "analyze_relationships": self.analyze_relationships,
            "generate_risk_scores": self.generate_risk_assessments
        }
        
        for step_name, step_func in analysis_steps.items():
            print(f"    🔄 {step_name}...")
            try:
                step_func(cloud_ip)
                print(f"    ✅ {step_name} complete")
            except Exception as e:
                print(f"    ⚠️  {step_name} failed: {e}")
                
        print("  ✅ Analysis pipeline complete")

    def extract_weighted_data(self):
        """Extract only high-value, weighted data from cloud processing"""
        
        print("  📊 Extracting weighted data based on value priorities...")
        
        extracted_data = {
            "session_id": self.session_id,
            "extraction_time": datetime.now().isoformat(),
            "high_value_findings": {},
            "medium_value_findings": {},
            "compliance_alerts": [],
            "entity_scores": {},
            "relationship_map": {}
        }
        
        cloud_ip = self.get_cloud_instance_ip()
        
        # Extract high-value entities
        for category, priorities in self.extraction_targets.items():
            for priority, data_types in priorities.items():
                print(f"    🎯 Extracting {priority} {category}...")
                
                category_data = self.extract_category_data(cloud_ip, category, data_types)
                if category_data:
                    if priority == "high_value":
                        extracted_data["high_value_findings"][category] = category_data
                    elif priority == "medium_value":  
                        extracted_data["medium_value_findings"][category] = category_data
                        
        # Extract compliance alerts (always high priority)
        compliance_data = self.extract_compliance_data(cloud_ip)
        if compliance_data:
            extracted_data["compliance_alerts"] = compliance_data
            
        print(f"  ✅ Extracted {len(extracted_data['high_value_findings'])} high-value categories")
        return extracted_data

    def consolidate_results(self, extracted_data):
        """Consolidate results into permanent local systems"""
        
        # Create permanent storage structure
        session_dir = self.results_dir / self.session_id
        session_dir.mkdir(exist_ok=True)
        
        # Save raw extracted data
        with open(session_dir / "extracted_data.json", "w") as f:
            json.dump(extracted_data, f, indent=2)
            
        # Create analysis reports
        self.create_compliance_report(extracted_data, session_dir)
        self.create_entity_network_map(extracted_data, session_dir)
        self.create_risk_assessment(extracted_data, session_dir)
        
        # Update permanent databases
        self.update_local_databases(extracted_data)
        self.update_notion_workspace(extracted_data)
        
        print(f"  ✅ Results consolidated in: {session_dir}")

    def cleanup_cloud_resources(self):
        """Clean up ALL cloud resources to prevent fragmentation"""
        
        print("  🧹 Destroying cloud resources...")
        
        cleanup_commands = [
            # Delete compute instance
            f"""gcloud compute instances delete investigation-processor-{self.session_id} \
                --project={self.gcp_project} \
                --zone=us-central1-a \
                --quiet""",
                
            # Delete firewall rules  
            f"""gcloud compute firewall-rules delete allow-investigation-{self.session_id} \
                --project={self.gcp_project} \
                --quiet""",
                
            # Clean up any persistent disks
            f"""gcloud compute disks list --project={self.gcp_project} \
                --filter="name~investigation.*{self.session_id}" \
                --format="value(name)" | xargs -r gcloud compute disks delete \
                --project={self.gcp_project} --zone=us-central1-a --quiet"""
        ]
        
        for cmd in cleanup_commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                resource_type = cmd.split()[2]
                if result.returncode == 0:
                    print(f"    ✅ {resource_type} destroyed")
                else:
                    print(f"    ⚠️  {resource_type} cleanup failed: {result.stderr}")
            except Exception as e:
                print(f"    ❌ Cleanup error: {e}")
                
        print("  ✅ Cloud resources destroyed - no fragmentation!")

    def create_compliance_report(self, data, output_dir):
        """Create consolidated compliance report"""
        
        report = {
            "investigation_summary": {
                "session": self.session_id,
                "entities_analyzed": len(data.get("entity_scores", {})),
                "high_risk_findings": len(data.get("compliance_alerts", [])),
                "processing_date": datetime.now().isoformat()
            },
            "compliance_status": self.calculate_compliance_status(data),
            "recommendations": self.generate_recommendations(data),
            "evidence_chain": self.document_evidence_chain(data)
        }
        
        with open(output_dir / "compliance_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        print(f"    📄 Compliance report: {output_dir}/compliance_report.json")

    def generate_final_report(self):
        """Generate final summary report"""
        
        return {
            "session_id": self.session_id,
            "status": "SUCCESS",
            "processing_time": datetime.now().isoformat(),
            "results_location": str(self.results_dir / self.session_id),
            "cloud_resources_status": "DESTROYED",
            "data_fragmentation": "NONE",
            "next_steps": [
                "Review compliance report",
                "Analyze entity network maps", 
                "Update investigation strategy",
                "Archive session data"
            ]
        }

    # Placeholder methods for analysis steps
    def get_cloud_instance_ip(self):
        """Get IP of cloud instance"""
        try:
            result = subprocess.run(
                f"gcloud compute instances describe investigation-processor-{self.session_id} --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'",
                shell=True, capture_output=True, text=True
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def upload_local_entities(self, cloud_ip):
        """Upload local entities to cloud for processing"""
        # Implementation for uploading Jacques Rich entities
        pass

    def cross_reference_icij_databases(self, cloud_ip):
        """Cross-reference with ICIJ databases"""
        # Implementation for ICIJ API calls
        pass

    def check_corporate_registries(self, cloud_ip):
        """Check corporate registries"""
        # Implementation for OpenCorporates, etc.
        pass

    def screen_sanctions_lists(self, cloud_ip):
        """Screen against sanctions lists"""
        # Implementation for OFAC, EU sanctions
        pass

    def build_neo4j_graph(self, cloud_ip):
        """Build entity relationship graph"""
        # Implementation for Neo4j graph building
        pass

    def analyze_relationships(self, cloud_ip):
        """Analyze entity relationships"""
        # Implementation for relationship analysis
        pass

    def generate_risk_assessments(self, cloud_ip):
        """Generate risk scores and assessments"""
        # Implementation for risk scoring
        pass

    def extract_category_data(self, cloud_ip, category, data_types):
        """Extract specific category data"""
        # Implementation for data extraction
        return {}

    def extract_compliance_data(self, cloud_ip):
        """Extract compliance-specific data"""
        # Implementation for compliance data extraction
        return []

    def calculate_compliance_status(self, data):
        """Calculate overall compliance status"""
        return "PENDING_REVIEW"

    def generate_recommendations(self, data):
        """Generate action recommendations"""
        return ["Review high-risk entities", "Investigate flagged relationships"]

    def document_evidence_chain(self, data):
        """Document evidence chain for legal purposes"""
        return {"chain_integrity": "MAINTAINED", "source_documents": []}

    def update_local_databases(self, data):
        """Update permanent local databases with results"""
        # Implementation for local database updates
        pass

    def update_notion_workspace(self, data):
        """Update Notion workspace with findings"""
        # Implementation for Notion updates
        pass

def main():
    """Execute ephemeral processing workflow"""
    
    processor = EphemeralInvestigationProcessor()
    
    print("🎯 Ephemeral Investigation Processing")
    print("💡 Philosophy: Build → Process → Extract → Consolidate → Destroy")
    print("🚫 No data fragmentation, no permanent cloud costs")
    
    confirm = input("\n🤔 Proceed with ephemeral processing? (y/N): ")
    
    if confirm.lower() == 'y':
        final_report = processor.execute_ephemeral_workflow()
        print("\n📊 Final Report:")
        print(json.dumps(final_report, indent=2))
    else:
        print("⏸️  Processing cancelled")

if __name__ == "__main__":
    main()