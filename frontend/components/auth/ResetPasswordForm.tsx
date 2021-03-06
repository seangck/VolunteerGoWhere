//lib
import { useFormik } from 'formik';
import * as yup from 'yup';
import axios from 'axios';
import { useState } from 'react';
//components
import SuccessAlert from '@/components/shared/SuccessAlert';
import ErrorAlert from '@/components/shared/ErrorAlert';
//mui
import { Button, TextField, Typography, Container, Stack } from '@mui/material';

/**
 * The yup validation for the reset password form
 */

const validationSchema = yup.object({
    password: yup.string().required('Password is required'),
});

interface ResetPasswordFormProps {
    email: string;
}

/**
 * Renders the reset password form
 *
 *
 * @returns {JSX.Element} - The reset password form
 */
const ResetPasswordForm = ({ email }: ResetPasswordFormProps): JSX.Element => {
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const formik = useFormik({
        initialValues: {
            email: email,
            password: '',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            try {
                setError('');
                const apiRes = await axios.post(`/api/auth/get_new_password_after_otp_verification/`, {
                    email: email,
                    password: values.password,
                });
                setSuccess(true);
                formik.resetForm();
            } catch (err: any) {
                setError(err.message);
            }
        },
    });

    return (
        <Container maxWidth='sm' sx={{ mt: 8 }}>
            <form onSubmit={formik.handleSubmit}>
                <Typography variant='h6' align='center'>
                    Reset Password
                </Typography>
                {error && <ErrorAlert>{error}</ErrorAlert>}
                {success && <SuccessAlert>Password reset successfully</SuccessAlert>}
                <TextField sx={{ mt: 2 }} fullWidth id='email' name='email' label='Email' value={email} disabled />

                <TextField
                    sx={{ mt: 2 }}
                    fullWidth
                    id='password'
                    name='password'
                    label='Password'
                    type='password'
                    value={formik.values.password}
                    onChange={formik.handleChange}
                    error={formik.touched.password && Boolean(formik.errors.password)}
                    helperText={formik.touched.password && formik.errors.password}
                />
                <Stack>
                    <Button
                        sx={{ mt: 1.4, width: '40%', backgroundColor: '#12CDD4' }}
                        color='primary'
                        variant='contained'
                        fullWidth
                        type='submit'
                        aria-label='send-otp'
                    >
                        Reset Password
                    </Button>
                </Stack>
            </form>
        </Container>
    );
};

export default ResetPasswordForm;
