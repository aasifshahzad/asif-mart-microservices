import os

directory = ["./inventory_service", "./notification_service",
             "./order_service", "./payment_service", "./product_service", "./user_service"]
old_filename = ".env.example"  # Replace with the current filename
new_filename = ".env"  # Replace with the new filename

for d_name in directory:
    old_file_path = os.path.join(d_name, old_filename)
    new_file_path = os.path.join(d_name, new_filename)

    # Rename the file
    os.rename(old_file_path, new_file_path)

    print(f"Renamed '{old_filename}' to '{new_filename}' in {d_name}")
