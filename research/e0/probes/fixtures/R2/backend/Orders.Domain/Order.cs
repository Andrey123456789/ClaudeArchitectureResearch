namespace Orders.Domain;

public sealed class Order
{
    public Guid Id { get; init; }

    public decimal Total { get; private set; }

    public void AddLine(decimal amount) => Total += amount;
}
