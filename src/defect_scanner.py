import argparse
import json
import time
import random
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.panel import Panel
from rich.layout import Layout
from rich import print

console = Console()


class FabricScanner:
    def __init__(self):
        self.defects = [
            "Leke",
            "Delik",
            "Dokuma Hatası",
            "Renk Uyuşmazlığı",
            "İplik Kopması",
        ]
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

    def run_simulation(self, duration_seconds=10, output_file=None):
        console.print(
            Panel.fit(
                "[bold cyan]Open Textile Intelligence[/bold cyan]\n[dim]Elit Komuta Merkezi - Kusur Tespit Modülü[/dim]",
                border_style="cyan",
            )
        )

        simulation_data = {"start_time": time.ctime(), "defects": [], "summary": {}}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task1 = progress.add_task("[green]Sensörler Kalibre Ediliyor...", total=100)

            # Calibration Simulation
            while not progress.finished:
                progress.update(task1, advance=1.5)
                time.sleep(0.02)

            task2 = progress.add_task(
                "[bold blue]Kumaş Rulosu Taranıyor...", total=duration_seconds * 10
            )

            table = Table(
                title="Canlı Tespit Akışı",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Zaman", style="dim", width=12)
            table.add_column("Kare NO", justify="right")
            table.add_column("Durum", justify="center")
            table.add_column("Kusur Tipi", style="red")
            table.add_column("Güven", justify="right")

            start_time = time.time()

            while time.time() - start_time < duration_seconds:
                frame_id = f"FR-{random.randint(10000, 99999)}"
                result = self.analyze_frame(frame_id)
                self.scanned_yards += 0.5

                status_icon = "✅ TAMAM"
                defect_info = "-"
                conf_str = "-"

                timestamp = time.strftime("%H:%M:%S")

                if result["detected"]:
                    self.defects_found += 1
                    status_icon = "⚠️ KUSUR"
                    defect_info = result["type"]
                    conf_str = f"{result['confidence']:.1%}"

                    table.add_row(
                        timestamp, frame_id, status_icon, defect_info, conf_str
                    )

                    simulation_data["defects"].append(
                        {
                            "timestamp": timestamp,
                            "frame_id": frame_id,
                            "type": defect_info,
                            "confidence": result["confidence"],
                        }
                    )

                progress.update(task2, advance=1)
                time.sleep(0.1)

            console.print(table)

            efficiency_score = max(100 - (self.defects_found * 2), 0)

            summary = Panel(
                f"[bold]Simülasyon Tamamlandı[/bold]\n"
                f"Toplam Taranan: [cyan]{self.scanned_yards:.1f} yarda[/cyan]\n"
                f"Bulunan Kusurlar: [red]{self.defects_found}[/red]\n"
                f"Verimlilik Oranı: [green]{efficiency_score}%[/green]",
                title="Analiz Raporu",
                border_style="green",
            )
            console.print(summary)

            simulation_data["summary"] = {
                "total_scanned_yards": self.scanned_yards,
                "total_defects": self.defects_found,
                "efficiency_score": efficiency_score,
                "end_time": time.ctime(),
            }

            if output_file:
                try:
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(simulation_data, f, ensure_ascii=False, indent=4)
                    console.print(
                        f"[bold green]Rapor dosyaya kaydedildi:[/bold green] {output_file}"
                    )
                except Exception as e:
                    console.print(f"[bold red]Rapor kaydedilemedi:[/bold red] {e}")


def advance(speed):
    return random.random() * speed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Open Textile Intelligence - Kumaş Kusur Simülasyonu"
    )
    parser.add_argument(
        "--duration", type=int, default=10, help="Simülasyon süresi (saniye)"
    )
    parser.add_argument(
        "--output", type=str, help="Raporun kaydedileceği JSON dosyası yolu"
    )

    args = parser.parse_args()

    try:
        scanner = FabricScanner()
        scanner.run_simulation(duration_seconds=args.duration, output_file=args.output)
    except KeyboardInterrupt:
        console.print("[bold red]Sistem Kullanıcı Tarafından Durduruldu[/bold red]")
