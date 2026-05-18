<script lang="ts">
    import { PUBLIC_API_URL } from "$env/static/public";
    import Logo from "$lib/components/Logo.svelte";
</script>

<div class="h-screen flex flex-col items-center justify-center -mt-4">
    <div class="flex flex-col items-center gap-6 border-2 border-fuchsia-400/30 rounded-2xl p-12 bg-black/50 backdrop-blur-md shadow-2xl sign">
        <div class="hidden sm:block"><Logo size="lg" /></div>
        <div class="sm:hidden"><Logo size="md" /></div>

        <div class="w-full border-t border-white/10"></div>

        <p class="text-white/40 text-sm italic text-center max-w-xs leading-relaxed">
            "If you've done six impossible things this morning, why not round it off with breakfast at Milliways?"
        </p>

        <div class="w-full border-t border-white/10"></div>

        <!-- Google sign-in button -->
        <a
            href="{PUBLIC_API_URL}/auth/login"
            class="flex items-center gap-3 bg-white text-gray-600 px-6 py-3 rounded-md shadow-md hover:shadow-lg transition-shadow font-medium text-sm"
        >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" class="w-5 h-5">
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                <path fill="none" d="M0 0h48v48H0z"/>
            </svg>
            Sign in with Google
        </a>
    </div>
</div>

<style>
    .sign {
        box-shadow:
            0 0 30px rgba(232, 121, 249, 0.15),
            0 0 60px rgba(167, 139, 250, 0.1),
            inset 0 0 30px rgba(0, 0, 0, 0.3);
    }

    .milliways {
        background: linear-gradient(to right, #e879f9, #4ade80, #a78bfa);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        filter:
            drop-shadow(0 0 8px rgba(232, 121, 249, 0.9))
            drop-shadow(0 0 20px rgba(232, 121, 249, 0.6))
            drop-shadow(0 0 40px rgba(167, 139, 250, 0.4));
    }

    .subtitle {
        color: #4ade80;
        text-shadow:
            0 0 7px #4ade80,
            0 0 15px #4ade80,
            0 0 30px #4ade80;
    }
</style>
