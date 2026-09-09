using LibraryAPI.Data;
using LibraryAPI.Repositories;
using LibraryAPI.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// 1. Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 2. Configure Entity Framework Core with SQL Server
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<LibraryDbContext>(options =>
{
    options.UseSqlServer(connectionString);
});

// 3. Register Dependency Injection Services
// Check database connectivity at startup; use InMemory fallback if SQL Server is not locally active
bool canConnectDb = false;
try
{
    var optionsBuilder = new DbContextOptionsBuilder<LibraryDbContext>();
    optionsBuilder.UseSqlServer(connectionString);
    using var tempContext = new LibraryDbContext(optionsBuilder.Options);
    canConnectDb = tempContext.Database.CanConnect();
    if (canConnectDb)
    {
        tempContext.Database.EnsureCreated();
    }
}
catch
{
    canConnectDb = false;
}

if (canConnectDb)
{
    Console.WriteLine("[Database]: Connected to SQL Server (LibraryDb_Week3). Using EF Core BookRepository.");
    builder.Services.AddScoped<IBookRepository, BookRepository>();
}
else
{
    Console.WriteLine("[Database]: SQL Server not detected or unreachable. Seamlessly using InMemoryBookRepository for live development.");
    builder.Services.AddSingleton<IBookRepository, InMemoryBookRepository>();
}

builder.Services.AddScoped<IBookService, BookService>();

// 4. Configure CORS for Angular Frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngular", policy =>
    {
        policy.WithOrigins("http://localhost:4200")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowAngular");
app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
