using LibraryAPI.Data;
using LibraryAPI.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

namespace LibraryAPI.Controllers
{
    public class LoginDto
    {
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }

    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly LibraryDbContext _context;

        public AuthController(LibraryDbContext context)
        {
            _context = context;
        }

        /// <summary>
        /// Skeleton login endpoint (Foundation for Week 4 JWT Authentication)
        /// </summary>
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginDto request)
        {
            if (string.IsNullOrWhiteSpace(request.Username) || string.IsNullOrWhiteSpace(request.Password))
            {
                return BadRequest(new { message = "Username and password are required." });
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == request.Username);
            
            // Dummy simulation for foundation check before Week 4 implementation
            if (user == null && request.Username != "admin")
            {
                return Unauthorized(new { message = "Invalid credentials. (Note: Auth placeholder will be fully wired in Week 4)" });
            }

            return Ok(new
            {
                message = "Authentication foundation verified successfully.",
                user = request.Username,
                role = user?.Role ?? "Admin",
                token = "PLACEHOLDER_TOKEN_WEEK4_IMPLEMENTATION"
            });
        }
    }
}
