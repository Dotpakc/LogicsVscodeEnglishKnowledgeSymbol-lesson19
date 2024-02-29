import g4f

response = g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", "content": "Хто такий Ілон Маск?"}],
    timeout=120,  # in secs
)

print(f"Result:", response)