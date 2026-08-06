import random
import time
import requests
import os
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

        # Battery recovery configuration
        self.battery_recovery_active = False
        self.battery_recovery_target = 95.0
        self.battery_recovery_rate = 5.0

        # Backend API endpoint
        self.api_url = os.getenv(
            "MISSIONVAULT_API_URL",
            "http://127.0.0.1:8000/telemetry"
        )

    def _normal_variation(self):
        """
        Generate realistic nominal telemetry variations.
        """

        # --------------------------------
        # Battery behavior
        # --------------------------------

        if self.battery_recovery_active:

            # Gradually recover battery after a temporary anomaly
            self.battery += self.battery_recovery_rate

            if self.battery >= self.battery_recovery_target:
                self.battery = self.battery_recovery_target
                self.battery_recovery_active = False

        else:

            # Normal battery consumption
            self.battery = max(
                0,
                self.battery - random.uniform(0.02, 0.08)
            )

        # --------------------------------
        # Temperature
        # --------------------------------

        self.temperature += random.uniform(-0.4, 0.4)

        self.temperature = max(
            18,
            min(35, self.temperature)
        )

        # --------------------------------
        # Signal strength
        # --------------------------------

        self.signal_strength += random.randint(-2, 2)

        self.signal_strength = max(
            -90,
            min(-60, self.signal_strength)
        )

        # --------------------------------
        # CPU load
        # --------------------------------

        self.cpu_load += random.uniform(-4, 4)

        self.cpu_load = max(
            10,
            min(50, self.cpu_load)
        )

        # --------------------------------
        # Payload
        # --------------------------------

        # Payload errors are temporary.
        # The payload returns to ACTIVE
        # during the next normal cycle.
        self.payload_status = "ACTIVE"

    def _inject_anomaly(self):
        """
        Occasionally simulate temporary satellite failures.
        """

        anomaly = random.choice([
            "temperature",
            "battery",
            "signal",
            "cpu",
            "payload"
        ])

        print(
            f"\n⚠ Injecting anomaly: {anomaly.upper()}"
        )

        # --------------------------------
        # Temperature anomaly
        # --------------------------------

        if anomaly == "temperature":

            self.temperature = random.uniform(
                90,
                100
            )

        # --------------------------------
        # Battery anomaly
        # --------------------------------

        elif anomaly == "battery":

            self.battery = random.uniform(
                5,
                20
            )

            # Activate temporary recovery mode
            self.battery_recovery_active = True

            print(
                "Battery recovery mode activated."
            )

        # --------------------------------
        # Signal anomaly
        # --------------------------------

        elif anomaly == "signal":

            self.signal_strength = random.randint(
                -120,
                -105
            )

        # --------------------------------
        # CPU anomaly
        # --------------------------------

        elif anomaly == "cpu":

            self.cpu_load = random.uniform(
                95,
                100
            )

        # --------------------------------
        # Payload anomaly
        # --------------------------------

        elif anomaly == "payload":

            self.payload_status = "ERROR"

    def generate(self):

        self.packet_count += 1

        # Generate normal telemetry variation
        self._normal_variation()

        # Roughly every 25 packets create an anomaly
        if self.packet_count % 25 == 0:

            self._inject_anomaly()

        telemetry = {
            "satellite_id": self.satellite_id,
            "battery": round(
                self.battery,
                2
            ),
            "temperature": round(
                self.temperature,
                2
            ),
            "signal_strength": self.signal_strength,
            "cpu_load": round(
                self.cpu_load,
                2
            ),
            "payload_status": self.payload_status,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

        return telemetry

    def send_telemetry(self, telemetry):
        """
        Send a telemetry packet
        to the MissionVault AI backend.
        """

        try:

            response = requests.post(
                self.api_url,
                json=telemetry,
                timeout=5
            )

            print(
                "\n=== TRANSMISSION RESULT ==="
            )

            print(
                f"Status Code : {response.status_code}"
            )

            print(
                f"Response    : {response.json()}"
            )

            print(
                "===========================\n"
            )

        except requests.exceptions.RequestException as error:

            print(
                "\nCould not connect to backend."
            )

            print(error)


def main():

    generator = TelemetryGenerator()

    print("=" * 60)
    print(
        "MissionVault AI - Satellite Telemetry Simulator"
    )
    print("=" * 60)

    while True:

        telemetry = generator.generate()

        print("\nTelemetry Packet")
        print("-" * 60)

        for key, value in telemetry.items():

            print(
                f"{key:18}: {value}"
            )

        generator.send_telemetry(
            telemetry
        )

        time.sleep(5)


if __name__ == "__main__":
    main()