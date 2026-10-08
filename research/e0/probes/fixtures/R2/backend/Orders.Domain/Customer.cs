namespace Orders.Domain;

public sealed class Customer
{
    public Guid Id { get; init; }

    public string Name { get; init; } = string.Empty;
}
