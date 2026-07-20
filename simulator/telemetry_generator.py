import random
import time
from datetime import datetime, timezone


class TelemetryGenerator:
    def __init__(self):
        self.satellite_id = "SD-CUBESAT-001"

        # Initial nominal values
        self.battery = 98.5
        self.temperature = 24.0
        self.signal_strength = -70
        self.cpu_load = 22.0
        self.payload_status = "ACTIVE"

        self.packet_count = 0

    def _normal_variation(self):
        """Generate realistic small changes."""

        self.battery = max(0, self.battery - random.uniform(0.02, 0.08))

        self.temperature += random.uniform(-0.4, 0.4)
        self.temperature = max(18, min(35, self.temperature))

        self.signal_strength += random.randint(-2, 2)
        self.signal_strength = max(-90, min(-60, self.signal_strength))

        self.cpu_load += random.uniform(-4, 4)
        self.cpu_load = max(10, min(50, self.cpu_load))

        self.payload_status = "ACTIVE"

    def _inject_anomaly(self):
        """Occasionally simulate satellite failures."""

        anomaly = random.choice([
            "temperature",
            "battery",
            "signal",
            "cpu",
            "payload"
        ])

        print(f"\n⚠ Injecting anomaly: {anomaly.upper()}")

        if anomaly == "temperature":
            self.temperature = random.uniform(90, 100)

        elif anomaly == "battery":
            self.battery = random.uniform(5, 20)

        elif anomaly == "signal":
            self.signal_strength = random.randint(-120, -105)

        elif anomaly == "cpu":
            self.cpu_load = random.uniform(95, 100)

        elif anomaly == "payload":
            self.payload_status = "ERROR"

    def generate(self):
        self.packet_count += 1

        self._normal_variation()

        # Roughly every 25 packets create an anomaly
        if self.packet_count % 25 == 0:
            self._inject_anomaly()

        telemetry = {
            "satellite_id": self.satellite_id,
            "battery": round(self.battery, 2),
            "temperature": round(self.temperature, 2),
            "signal_strength": self.signal_strength,
            "cpu_load": round(self.cpu_load, 2),
            "payload_status": self.payload_status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        return telemetry


def main():
    generator = TelemetryGenerator()

    print("=" * 60)
    print("MissionVault AI - Satellite Telemetry Simulator")
    print("=" * 60)

    while True:
        telemetry = generator.generate()

        print("\nTelemetry Packet")
        print("-" * 60)

        for key, value in telemetry.items():
            print(f"{key:18}: {value}")

        time.sleep(5)


if __name__ == "__main__":
    main()