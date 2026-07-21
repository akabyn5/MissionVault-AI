telemetry_storage = []

def save_telemetry(data):
    telemetry_storage.append(data)

    print(f"Stored packets: {len(telemetry_storage)}")
    print(f"Latest packet: {telemetry_storage[-1]}")

    return data