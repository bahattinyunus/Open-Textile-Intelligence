import time
import random
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.layout import Layout
from rich import print

console = Console()

class FabricScanner:
    def __init__(self):
        self.defects = ["Stain", "Hole", "Weave Error", "Color Mismatch", "Thread Break"]
        self.scanned_yards = 0
        self.defects_found = 0

    def analyze_frame(self, frame_id):
        """Simulates analyzing a single frame of fabric."""
        is_defective = random.random() < 0.15  # 15% chance of defect
        
        if is_defective:
            defect_type = random.choice(self.defects)
            confidence = random.uniform(0.85, 0.99)
            return {"detected": True, "type": defect_type, "confidence": confidence}
        return {"detected": False}

    def run_simulation(self, duration_seconds=10):
        console.print(Panel.fit("[bold cyan]Open Textile Intelligence[/bold cyan]\n[dim]Elite Command Center - Defect Detection Module[/dim]", border_style="cyan"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task1 = progress.add_task("[green]Calibrating Sensors...", total=100)
            
            # Calibration Simulation
            while not progress.finished:
                progress.update(task1, advance(1.5))
                time.sleep(0.02)
                
            task2 = progress.add_task("[bold blue]Scanning Fabric Roll...", total=duration_seconds*10)

            table = Table(title="Live Detection Feed", show_header=True, header_style="bold magenta")
            table.add_column("Time", style="dim", width=12)
            table.add_column("Frame ID", justify="right")
            table.add_column("Status", justify="center")
            table.add_column("Defect Type", style="red")
            table.add_column("Confidence", justify="right")

            start_time = time.time()
            
            while time.time() - start_time < duration_seconds:
                frame_id = f"FR-{random.randint(10000, 99999)}"
                result = self.analyze_frame(frame_id)
                self.scanned_yards += 0.5
                
                status_icon = "✅ OK"
                defect_info = "-"
                conf_str = "-"
                
                if result["detected"]:
                    self.defects_found += 1
                    status_icon = "⚠️ DEFECT"
                    defect_info = result["type"]
                    conf_str = f"{result['confidence']:.1%}"
                    
                    table.add_row(
                        time.strftime("%H:%M:%S"), 
                        frame_id, 
                        status_icon, 
                        defect_info, 
                        conf_str
                    )
                    
                progress.update(task2, advance=1)
                time.sleep(0.1)

            console.print(table)
            
            summary = Panel(
                f"[bold]Simulation Complete[/bold]\n"
                f"Total Scanned: [cyan]{self.scanned_yards:.1f} yards[/cyan]\n"
                f"Defects Found: [red]{self.defects_found}[/red]\n"
                f"Efficiency Rating: [green]{max(100 - (self.defects_found * 2), 0)}%[/green]",
                title="Analysis Report",
                border_style="green"
            )
            console.print(summary)

def advance(speed):
    return random.random() * speed

if __name__ == "__main__":
    try:
        scanner = FabricScanner()
        scanner.run_simulation()
    except KeyboardInterrupt:
        console.print("[bold red]System Halted by User[/bold red]")
